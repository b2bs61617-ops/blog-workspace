"""tools/配下の各スクリプトはパッケージ化されていない単発ファイルなので、
それぞれの置き場所をsys.pathに足して `import x_monitor` のように直接importできるようにする。
"""
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent

for p in (TOOLS_DIR, TOOLS_DIR / "koikeyz-monitor", TOOLS_DIR / "Xiy", TOOLS_DIR / "x-trend-monitor", TOOLS_DIR / "youtube-talent-monitor", TOOLS_DIR / "shorts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
