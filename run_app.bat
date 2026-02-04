@echo off
echo Starting Legal Eagle AI...

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Install dependencies
echo Installing/Verifying dependencies...
pip install --upgrade streamlit google-generativeai pymupdf python-dotenv
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies.
    echo This usually happens if the app is already running or a file is locked.
    echo Please CLOSE ALL terminal windows and try again.
    pause
    exit /b %errorlevel%
)

REM Run App
echo Launching Application...
streamlit run app.py
