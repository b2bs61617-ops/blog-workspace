"""X(旧Twitter)・Instagramの投稿URLから動画クリップをダウンロードするツール。

TikTok/YouTube Shorts向けショート動画自動生成パイプライン(shorts-videoスキル)の
STEP2で使う。ダウンロード先(tools/shorts/downloads/)は著作権のある動画素材のため
.gitignoreでGit管理外にしている(tools/youtube-talent-monitorのframes/と同じ考え方)。

前提: yt-dlpが必要(`pip install yt-dlp`)。セットアップ手順はdocs/shorts-video-setup.md参照。

使い方:
  python tools/shorts/clip_downloader.py --url "https://x.com/xxx/status/123" --slug matsuda_genta_jordan
  python tools/shorts/clip_downloader.py --url "https://x.com/xxx/status/123" --out tools/shorts/downloads/xxx/clip_01.mp4

他のスクリプトから使う場合:
  from clip_downloader import download_clip, next_clip_path
"""
import argparse
import re
import sys
import time
from pathlib import Path

try:
    import yt_dlp
    YTDLP_OK = True
except ImportError:
    YTDLP_OK = False

ROOT = Path(__file__).resolve().parent.parent.parent
DOWNLOADS_DIR = Path(__file__).resolve().parent / "downloads"


def detect_source(url: str) -> str:
    """投稿URLがX/Instagramどちらの由来か判定する(不明ならunknown)。"""
    if re.search(r"(?:^|//)(?:www\.)?(?:x\.com|twitter\.com)/", url):
        return "x"
    if re.search(r"(?:^|//)(?:www\.)?instagram\.com/", url):
        return "instagram"
    return "unknown"


def next_clip_path(downloads_dir: Path, slug: str) -> Path:
    """指定slug配下で未使用のclip_NN.mp4パスを返す(既存ファイルとの衝突を避ける)。"""
    target_dir = downloads_dir / slug
    existing = sorted(target_dir.glob("clip_*.mp4")) if target_dir.exists() else []
    used_numbers = set()
    for f in existing:
        m = re.match(r"clip_(\d+)\.mp4$", f.name)
        if m:
            used_numbers.add(int(m.group(1)))
    n = 1
    while n in used_numbers:
        n += 1
    return target_dir / f"clip_{n:02d}.mp4"


def download_clip(url: str, out_path: Path, retries: int = 3) -> Path:
    """yt-dlpで動画をダウンロードし、実際に保存されたパスを返す。"""
    if not YTDLP_OK:
        raise RuntimeError("yt-dlpが未インストールだワン: pip install yt-dlp")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": str(out_path.with_suffix("")) + ".%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 60,
        "retries": 5,
        "fragment_retries": 5,
    }

    last_err = None
    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            last_err = None
            break
        except Exception as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(5)

    if last_err:
        source = detect_source(url)
        hint = ""
        if source == "instagram":
            hint = "(Instagramは非公開/ログイン必須の投稿だとyt-dlp単体では落とせないことがあるワン。その場合は手動でダウンロードしてtools/shorts/downloads/配下に置いてほしいワン)"
        raise RuntimeError(f"動画DL失敗だワン: {last_err} {hint}")

    downloaded = list(out_path.parent.glob(out_path.stem + ".*"))
    if not downloaded:
        raise RuntimeError("ダウンロードは成功したはずだが、ファイルが見つからなかったワン")
    return downloaded[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="X/Instagramの投稿から動画をダウンロードする")
    parser.add_argument("--url", required=True, help="投稿URL")
    parser.add_argument("--out", help="保存先パス(指定しなければ--slugから自動決定)")
    parser.add_argument("--slug", help="記事slug(--out省略時に tools/shorts/downloads/{slug}/clip_NN.mp4 を使う)")
    args = parser.parse_args()

    if args.out:
        out_path = Path(args.out)
    elif args.slug:
        out_path = next_clip_path(DOWNLOADS_DIR, args.slug)
    else:
        print("エラー: --out か --slug のどちらかを指定してほしいワン")
        sys.exit(1)

    try:
        saved = download_clip(args.url, out_path)
    except RuntimeError as e:
        print(f"エラー: {e}")
        sys.exit(1)

    print(f"保存したワン: {saved}")
