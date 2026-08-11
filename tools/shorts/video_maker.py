"""ダウンロード済みクリップから縦型(9:16)ショート動画を作るツール。

TikTok/YouTube Shorts向けショート動画自動生成パイプライン(shorts-videoスキル)の
STEP3で使う。各クリップを1080x1920にスケール+パディングして結合し、冒頭にフック文の
テキストオーバーレイを焼き込み、60秒以内にトリムする。BGMは--bgmで音源ファイルを渡した
場合のみミックスする(著作権フリー音源は同梱していないので、トモキが用意したファイルを
指定する運用)。

前提: ffmpegが必要(`brew install ffmpeg`)。セットアップ手順はdocs/shorts-video-setup.md参照。

使い方:
  python tools/shorts/video_maker.py --clips tools/shorts/downloads/xxx/clip_01.mp4 \\
      --text "これマジ!?" --out tools/shorts/output/xxx.mp4
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_FONT = REPO_ROOT / "assets" / "fonts" / "MPLUSRounded1c-Black.ttf"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def escape_drawtext(text: str) -> str:
    """ffmpegのdrawtextフィルタ用にテキストをエスケープする(バックスラッシュ・コロン・%)。
    シングルクオートはffmpegのフィルタ構文と衝突しやすいため全角に置換して回避する。
    """
    text = text.replace("\\", "\\\\")
    text = text.replace(":", "\\:")
    text = text.replace("%", "\\%")
    text = text.replace("'", "’")
    return text


def vertical_scale_pad_filter(width: int = 1080, height: int = 1920) -> str:
    """入力サイズによらず縦型{width}x{height}に収める(アスペクト比維持+黒帯パディング)フィルタ文字列。"""
    return (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1"
    )


def build_drawtext_filter(text: str, font_path: Path, fontsize: int = 64, y_expr: str = "120", box: bool = True) -> str:
    """フック文を焼き込むdrawtextフィルタ文字列を組み立てる。"""
    opts = [
        f"fontfile='{font_path}'",
        f"text='{escape_drawtext(text)}'",
        f"fontsize={fontsize}",
        "fontcolor=white",
        "x=(w-text_w)/2",
        f"y={y_expr}",
    ]
    if box:
        opts += ["box=1", "boxcolor=black@0.55", "boxborderw=20"]
    return "drawtext=" + ":".join(opts)


def clamp_duration(total_seconds: float, max_seconds: float = 60) -> float:
    """尺をTikTok/Shorts向けの上限内に収める(それ以下ならそのまま)。"""
    return min(total_seconds, max_seconds)


def build_ffmpeg_command(
    clips: list[Path],
    output_path: Path,
    overlay_text: str,
    font_path: Path = DEFAULT_FONT,
    bgm_path: Path | None = None,
    max_seconds: float = 60,
    width: int = 1080,
    height: int = 1920,
) -> list[str]:
    """クリップ結合+縦型変換+テキストオーバーレイ+(任意)BGMミックスのffmpegコマンドを組み立てる。"""
    if not clips:
        raise ValueError("clipsが空だワン")

    scale_filter = vertical_scale_pad_filter(width, height)

    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    if bgm_path:
        inputs += ["-i", str(bgm_path)]

    filter_parts = []
    concat_labels = ""
    for i in range(len(clips)):
        filter_parts.append(f"[{i}:v]{scale_filter}[v{i}]")
        concat_labels += f"[v{i}][{i}:a]"
    filter_parts.append(f"{concat_labels}concat=n={len(clips)}:v=1:a=1[vcat][acat]")

    text_filter = build_drawtext_filter(overlay_text, font_path)
    filter_parts.append(f"[vcat]{text_filter}[vout]")

    maps = ["-map", "[vout]"]
    if bgm_path:
        bgm_index = len(clips)
        filter_parts.append(f"[acat][{bgm_index}:a]amix=inputs=2:duration=first:dropout_transition=2[aout]")
        maps += ["-map", "[aout]"]
    else:
        maps += ["-map", "[acat]"]

    filter_complex = ";".join(filter_parts)

    return (
        ["ffmpeg", "-y"] + inputs
        + ["-filter_complex", filter_complex]
        + maps
        + ["-t", str(clamp_duration(max_seconds, max_seconds))]
        + ["-c:v", "libx264", "-c:a", "aac", "-movflags", "+faststart"]
        + [str(output_path)]
    )


def make_video(
    clips: list[Path],
    output_path: Path,
    overlay_text: str,
    font_path: Path = DEFAULT_FONT,
    bgm_path: Path | None = None,
    max_seconds: float = 60,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_ffmpeg_command(clips, output_path, overlay_text, font_path, bgm_path, max_seconds)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg失敗だワン: {result.stderr[-2000:]}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="クリップから縦型ショート動画を作る")
    parser.add_argument("--clips", nargs="+", required=True, help="入力クリップ(1本以上、結合される)")
    parser.add_argument("--text", required=True, help="冒頭に焼き込むフック文")
    parser.add_argument("--out", help="出力パス(省略時はtools/shorts/output/配下に自動命名)")
    parser.add_argument("--bgm", help="BGM音源ファイル(省略時はBGMなし)")
    parser.add_argument("--max-seconds", type=float, default=60)
    args = parser.parse_args()

    clip_paths = [Path(c) for c in args.clips]
    for c in clip_paths:
        if not c.exists():
            print(f"エラー: クリップが見つからないワン: {c}")
            sys.exit(1)

    out_path = Path(args.out) if args.out else OUTPUT_DIR / (clip_paths[0].parent.name + ".mp4")
    bgm_path = Path(args.bgm) if args.bgm else None

    try:
        saved = make_video(clip_paths, out_path, args.text, bgm_path=bgm_path, max_seconds=args.max_seconds)
    except RuntimeError as e:
        print(f"エラー: {e}")
        sys.exit(1)

    print(f"作ったワン: {saved}")
