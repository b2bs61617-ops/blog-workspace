"""YouTube動画から代表フレームを抜き出し、Geminiで服装・アクセサリー・ロケ地の特徴を解析する。

文字起こしでは「会話内容」しか分からず、視聴者(オタク)が知りたい服装・アクセサリー・
訪問場所は映像を見ないと分からないため、フレーム画像+Vision対応AIで補う(2026-07-29導入)。

ffmpeg不要の設計: yt-dlpで低解像度(480p以下)の直リンクを取得し、opencv-pythonの
VideoCapture.set(CAP_PROP_POS_MSEC)でシークしてキャプチャする(動画をディスクに
フルダウンロードしない)。Gemini呼び出しはkoikeyz-monitor(x_monitor.py)と同じ
google-genai SDK・gemini-2.5-flashを流用(トモキ指示によりClaude/マツは介さず、
このスクリプト単体で完結させる。日次の自動監視から直接呼ばれる想定)。

抽出したフレームは frames/{video_id}/ に保存して残す(2026-07-29時点の方針。
運用しながら見直す可能性あり)。Gitには含めない(著作権のある動画フレーム画像のため
リポジトリに含めるべきではない。.gitignore参照)。

実行(単体テスト用):
  python tools/youtube-talent-monitor/visual_analysis.py <video_idまたはURL> [<動画タイトル>]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
REPO_ROOT = ROOT.parent.parent
FRAMES_DIR = ROOT / "frames"

FRAME_COUNT = 12            # 1動画あたり抽出するフレーム数
FRAME_MIN_FRACTION = 0.05   # 動画の最初(オープニング)は情報価値が低いため除外
FRAME_MAX_FRACTION = 0.95   # 動画の最後(エンディング)も同様に除外
STREAM_FORMAT = "best[height<=480][ext=mp4]/best[height<=480]"
GEMINI_MODEL = "gemini-2.5-flash"

VISION_PROMPT_TEMPLATE = """以下はYouTube動画「{title}」から一定間隔で抜き出した{count}枚の画像です。
この動画に出演している旧ジャニーズ/STARTO所属タレントについて、ブログ記事の参考情報として次の観点を日本語で箇条書きにしてください。

【服装】トップス・ボトムス・アウター・靴の特徴や色、ブランドロゴが見えるかどうか
【アクセサリー】ネックレス・ピアス・時計・指輪・帽子など身につけている小物
【ロケーション】屋内か屋外か、画面に映る看板・店名・地名・案内板などの文字情報、特徴的な建物や風景(ランドマークになりそうなもの)

情報が読み取れない項目は「不明」で構いません。憶測で断定せず、画像から読み取れる範囲で書いてください。"""


def compute_timestamps(duration_sec, count=FRAME_COUNT, min_frac=FRAME_MIN_FRACTION, max_frac=FRAME_MAX_FRACTION):
    """動画長からフレーム取得タイムスタンプ(秒)を均等割りで返す(純粋関数)。
    min_frac〜max_fracの範囲に絞ることで冒頭・末尾のオープニング/エンディングを避ける。"""
    if duration_sec <= 0 or count <= 0:
        return []
    if count == 1:
        return [duration_sec * (min_frac + max_frac) / 2]
    span = max_frac - min_frac
    return [duration_sec * (min_frac + span * i / (count - 1)) for i in range(count)]


def build_vision_prompt(title, count):
    """Gemini Visionに渡すプロンプトを組み立てる(純粋関数)。"""
    return VISION_PROMPT_TEMPLATE.format(title=title, count=count)


def load_gemini_api_key():
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return None
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip() or None
    return None


def get_stream_info(video_id):
    """yt-dlpで低解像度の直リンクと動画長(秒)を取得する(フルダウンロードはしない)。"""
    import yt_dlp

    ydl_opts = {"quiet": True, "no_warnings": True, "format": STREAM_FORMAT}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
    return info["url"], info.get("duration") or 0


def extract_frames(stream_url, timestamps):
    """opencvでシークしてフレームを取得し、[(timestamp, jpg_bytes), ...]を返す(取得失敗分はスキップ)。"""
    import cv2

    frames = []
    cap = cv2.VideoCapture(stream_url)
    try:
        if not cap.isOpened():
            return frames
        for ts in timestamps:
            cap.set(cv2.CAP_PROP_POS_MSEC, ts * 1000)
            ok, frame = cap.read()
            if not ok:
                continue
            ok, buf = cv2.imencode(".jpg", frame)
            if ok:
                frames.append((ts, buf.tobytes()))
    finally:
        cap.release()
    return frames


def save_frames(video_id, frames):
    """フレームをframes/{video_id}/に保存し、保存先パスのリストを返す。"""
    out_dir = FRAMES_DIR / video_id
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, (ts, jpg_bytes) in enumerate(frames):
        path = out_dir / f"frame_{i:02d}_{int(ts)}s.jpg"
        path.write_bytes(jpg_bytes)
        paths.append(path)
    return paths


def analyze_frames_with_gemini(frame_paths, title, api_key):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    parts = [types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg") for p in frame_paths]
    prompt = build_vision_prompt(title, len(frame_paths))
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[*parts, prompt],
    )
    return response.text.strip()


def analyze_video_visuals(video_id, title):
    """動画1本の視覚解析(フレーム抽出+Gemini解析)をまとめて行う。
    APIキー未設定・取得失敗などどこかで失敗したらNoneを返す(呼び出し側の通知は止めない)。"""
    api_key = load_gemini_api_key()
    if not api_key:
        print("  画像解析スキップ: .envにGEMINI_API_KEYが未設定")
        return None
    try:
        stream_url, duration = get_stream_info(video_id)
        timestamps = compute_timestamps(duration)
        frames = extract_frames(stream_url, timestamps)
        if not frames:
            print(f"  画像解析スキップ({video_id}): フレームを1枚も取得できなかった")
            return None
        frame_paths = save_frames(video_id, frames)
        notes = analyze_frames_with_gemini(frame_paths, title, api_key)
        return {"visual_notes": notes, "frame_paths": [str(p) for p in frame_paths]}
    except Exception as e:
        print(f"  画像解析失敗({video_id}): {type(e).__name__}: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python visual_analysis.py <video_idまたはURL> [<動画タイトル>]")
        sys.exit(1)
    vid = sys.argv[1].rsplit("v=", 1)[-1].rsplit("/", 1)[-1]
    title = sys.argv[2] if len(sys.argv) > 2 else vid
    result = analyze_video_visuals(vid, title)
    print(json.dumps(result, ensure_ascii=False, indent=2) if result else "解析失敗")
