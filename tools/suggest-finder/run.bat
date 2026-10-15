@echo off
setlocal
rem Suggest finder: double-click and type a name. Extra args are passed through (e.g. run.bat --max 50)
rem Works on every team PC: finds Python, installs missing packages on first run.
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

rem Resolve Python explicitly so the WindowsApps store stub cannot shadow it.
set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not exist "%PY%" set "PY=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not exist "%PY%" set "PY=python"

"%PY%" -c "import requests, playwright, google.genai" 2>nul
if errorlevel 1 (
  echo First run: installing required packages...
  "%PY%" -m pip install --quiet requests playwright google-genai
  "%PY%" -m playwright install chromium
)

"%PY%" "%~dp0suggest_finder.py" %*
pause
endlocal
