@echo off
cd /d "%~dp0"
where pythonw >nul 2>nul
if %errorlevel%==0 (
    pythonw x_collector.py
) else (
    py -3 x_collector.py
)
