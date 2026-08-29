@echo off
rem 24時間マラソン現在地トラッカー 手動実行
cd /d "%~dp0..\.."
python tools\marathon-tracker\tracker.py %*
