@echo off
REM Lab Control System - One-Click Client Installer
REM Clients can download and run this single file

echo ========================================
echo  Lab Control System - Auto Installer
echo ========================================
echo.

REM Get server IP from user
set /p SERVER_IP="Enter Lab Control Server IP: "
set /p SYSTEM_ID="Enter your System ID: "

echo.
echo Installing Python dependencies...
pip install psutil requests --quiet

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Please install Python and try again
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Create monitoring agent script
echo Creating monitoring agent...

echo import psutil > monitoring_agent.py
echo import requests >> monitoring_agent.py
echo import socket >> monitoring_agent.py
echo import argparse >> monitoring_agent.py
echo import time >> monitoring_agent.py
echo import json >> monitoring_agent.py
echo from datetime import datetime >> monitoring_agent.py
echo. >> monitoring_agent.py
echo class SystemMonitor: >> monitoring_agent.py
echo     def __init__(self, system_id, server_url): >> monitoring_agent.py
echo         self.system_id = system_id >> monitoring_agent.py
echo         self.server_url = server_url.rstrip('/') >> monitoring_agent.py
echo         self.api_endpoint = f"{self.server_url}/api/systems/{system_id}/health" >> monitoring_agent.py
echo. >> monitoring_agent.py
echo     def get_system_health(self): >> monitoring_agent.py
echo         try: >> monitoring_agent.py
echo             cpu_usage = psutil.cpu_percent(interval=1) >> monitoring_agent.py
echo             memory = psutil.virtual_memory() >> monitoring_agent.py
echo             memory_usage = memory.percent >> monitoring_agent.py
echo             disk = psutil.disk_usage('/') >> monitoring_agent.py
echo             disk_usage = disk.percent >> monitoring_agent.py
echo             status = "Online" >> monitoring_agent.py
echo             health_status = "Healthy" >> monitoring_agent.py
echo             if cpu_usage ^> 90 or memory_usage ^> 90 or disk_usage ^> 95: >> monitoring_agent.py
echo                 health_status = "Warning" >> monitoring_agent.py
echo             return { >> monitoring_agent.py
echo                 'status': status, >> monitoring_agent.py
echo                 'health_status': health_status, >> monitoring_agent.py
echo                 'cpu_usage': cpu_usage, >> monitoring_agent.py
echo                 'memory_usage': memory_usage, >> monitoring_agent.py
echo                 'disk_usage': disk_usage, >> monitoring_agent.py
echo                 'timestamp': datetime.now().isoformat() >> monitoring_agent.py
echo             } >> monitoring_agent.py
echo         except Exception as e: >> monitoring_agent.py
echo             return None >> monitoring_agent.py
echo. >> monitoring_agent.py
echo     def report_health(self): >> monitoring_agent.py
echo         health_data = self.get_system_health() >> monitoring_agent.py
echo         if not health_data: >> monitoring_agent.py
echo             return False >> monitoring_agent.py
echo         try: >> monitoring_agent.py
echo             response = requests.post( >> monitoring_agent.py
echo                 self.api_endpoint, >> monitoring_agent.py
echo                 json=health_data, >> monitoring_agent.py
echo                 timeout=5 >> monitoring_agent.py
echo             ) >> monitoring_agent.py
echo             return response.status_code == 200 >> monitoring_agent.py
echo         except: >> monitoring_agent.py
echo             return False >> monitoring_agent.py
echo. >> monitoring_agent.py
echo     def start_monitoring(self, interval=30): >> monitoring_agent.py
echo         print(f"🚀 Starting monitoring for system {self.system_id}") >> monitoring_agent.py
echo         print(f"📡 Server: {self.server_url}") >> monitoring_agent.py
echo         print("-" * 50) >> monitoring_agent.py
echo         try: >> monitoring_agent.py
echo             while True: >> monitoring_agent.py
echo                 if self.report_health(): >> monitoring_agent.py
echo                     print(f"✅ [{datetime.now().strftime('%%H:%%M:%%S')}] Health reported") >> monitoring_agent.py
echo                 else: >> monitoring_agent.py
echo                     print(f"❌ [{datetime.now().strftime('%%H:%%M:%%S')}] Report failed") >> monitoring_agent.py
echo                 time.sleep(interval) >> monitoring_agent.py
echo         except KeyboardInterrupt: >> monitoring_agent.py
echo             print("\\n⏹️ Monitoring stopped") >> monitoring_agent.py
echo. >> monitoring_agent.py
echo if __name__ == "__main__": >> monitoring_agent.py
echo     monitor = SystemMonitor(%SYSTEM_ID%, "http://%SERVER_IP%:5000") >> monitoring_agent.py
echo     monitor.start_monitoring() >> monitoring_agent.py

echo ✅ Agent created
echo.

echo ========================================
echo 🎉 INSTALLATION COMPLETE!
echo ========================================
echo.
echo Your PC is now monitoring system ID: %SYSTEM_ID%
echo Server: http://%SERVER_IP%:5000
echo.
echo The agent will start monitoring in 3 seconds...
echo Press Ctrl+C to stop monitoring
echo.

timeout /t 3 /nobreak >nul

echo 🚀 Starting monitoring...
python monitoring_agent.py