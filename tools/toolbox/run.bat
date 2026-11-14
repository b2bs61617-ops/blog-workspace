@echo off
rem Matsu toolbox launcher (ASCII only: Japanese text here breaks cmd.exe)
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0..\.."
set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not exist "%PY%" set "PY=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if exist "%PY%" goto run
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 tools\toolbox\toolbox.py %*
  goto end
)
set "PY=python"
:run
"%PY%" tools\toolbox\toolbox.py %*
:end
if errorlevel 1 pause
