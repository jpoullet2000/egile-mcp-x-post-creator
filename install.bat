@echo off
echo Installing egile-mcp-x-post-creator...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install the package in editable mode
echo Installing package and dependencies...
pip install -e .

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your X/Twitter API credentials!
)

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your X/Twitter API credentials
echo 2. Run the server with: python -m egile_mcp_x_post_creator
echo.
pause
