@echo off
setlocal
rem 24h marathon location tracker - manual / scheduled-task entry point.
rem Force UTF-8 because the default Windows console codepage is cp932.
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

rem Resolve Python explicitly so the WindowsApps store stub cannot shadow it.
set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not exist "%PY%" set "PY=python"

cd /d "%~dp0..\.."
"%PY%" tools\marathon-tracker\tracker.py %*
endlocal
