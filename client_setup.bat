@echo off
REM Lab Control System Client Setup for Windows
REM Run this as Administrator

echo ========================================
echo  Lab Control System - Client Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies
echo Installing monitoring dependencies...
pip install psutil requests

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ CLIENT SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Copy monitoring_agent.py to this machine
echo 2. Get your System ID from the Lab Control Server
echo 3. Run the monitoring agent:
echo.
echo    python monitoring_agent.py --system-id YOUR_ID --server http://SERVER_IP:5000
echo.
echo Example:
echo    python monitoring_agent.py --system-id 2 --server http://192.168.1.100:5000
echo.
echo The agent will monitor this PC and report to your server every 30 seconds.
echo.
pause