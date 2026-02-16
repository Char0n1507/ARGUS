@echo off
REM ARGUS Dashboard Launcher for Windows

if not exist "venv" (
    echo [WARNING] Virtual Environment not found! Please run setup first.
    pause
    exit /b 1
)

echo [INFO] Launching ARGUS Command Center...
call venv\Scripts\activate
streamlit run dashboard.py
pause
