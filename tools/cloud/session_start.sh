#!/usr/bin/env bash
# SessionStart hook for Claude Code on the web (runs only when CLAUDE_CODE_REMOTE=true).
# Prepares .env, Python packages, Japanese fonts and Chromium for the blog tools.
cd "$(dirname "$0")/../.." || exit 0

python3 tools/cloud/make_env.py

python3 -c "import requests, PIL, playwright" 2>/dev/null || \
  pip install -q requests pillow playwright >/dev/null 2>&1

# Eyecatch HTML uses Yu Gothic/Meiryo; on Linux fall back to Noto CJK.
if ! fc-list 2>/dev/null | grep -qi "Noto Sans CJK"; then
  (apt-get install -y -q fonts-noto-cjk >/dev/null 2>&1 || \
   (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q fonts-noto-cjk >/dev/null 2>&1)) || \
   echo "[cloud] 日本語フォントの導入に失敗したワン(アイキャッチが文字化けするかも)"
fi

python3 - <<'EOF' 2>/dev/null || python3 -m playwright install --with-deps chromium >/dev/null 2>&1
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()
EOF

echo "[cloud] クラウド環境の準備ができたワン"
exit 0
