#!/bin/bash
# Matsu toolbox launcher for Mac (double-click in Finder)
cd "$(dirname "$0")/../.." || exit 1
export PYTHONUTF8=1
exec python3 tools/toolbox/toolbox.py "$@"
