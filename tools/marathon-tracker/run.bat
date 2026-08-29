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

rem Keep a daily log so scheduled runs (whose console is discarded) are debuggable.
if not exist "tools\marathon-tracker\logs" mkdir "tools\marathon-tracker\logs"
for /f "tokens=1-3 delims=/-. " %%a in ("%date%") do set "TODAY=%%a%%b%%c"
set "LOGF=tools\marathon-tracker\logs\run_%TODAY%.log"
set "TMPF=%TEMP%\mtrun_%RANDOM%.txt"

"%PY%" tools\marathon-tracker\tracker.py %* > "%TMPF%" 2>&1
type "%TMPF%"
>> "%LOGF%" echo ---------- %date% %time% ----------
type "%TMPF%" >> "%LOGF%"
del "%TMPF%" 2>nul
endlocal
