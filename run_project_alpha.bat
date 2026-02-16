@echo off
TITLE Project Alpha Launcher
CLS

ECHO ======================================================
ECHO         Project Alpha - Cybersecurity Tool
ECHO ======================================================
ECHO.
ECHO [1] Installing Dependencies (This may take a moment)...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERROR] Failed to install dependencies.
    PAUSE
    EXIT /B
)

ECHO.
ECHO [SUCCESS] Dependencies installed.
ECHO.
ECHO Select Mode:
ECHO [1] Train Model (Capture normal traffic)
ECHO [2] Start Detection (Real-time)
ECHO [3] Launch Dashboard (Web UI)
ECHO [4] Generate PDF Report (Manager Briefing)

SET /P "Mode=Type 1, 2, 3, or 4 then press ENTER: "

IF "%Mode%"=="1" (
    ECHO.
    ECHO Starting Training Mode...
    ECHO Please browse the web/generate traffic for 30 seconds...
    python -m project_alpha.main --train
) ELSE IF "%Mode%"=="2" (
    ECHO.
    ECHO Starting Detection Mode...
    ECHO Press Ctrl+C to stop.
    python -m project_alpha.main --detect
) ELSE IF "%Mode%"=="3" (
    ECHO.
    ECHO Launching Dashboard...
    start python -m streamlit run dashboard.py
) ELSE IF "%Mode%"=="4" (
    ECHO.
    python -m project_alpha.src.reporting
    PAUSE
) ELSE (
    ECHO Invalid selection.
)

PAUSE
