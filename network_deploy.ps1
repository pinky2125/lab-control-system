# Lab Control System - Network Deployment Script
# Run this on the server to deploy to multiple client PCs
# Requires PowerShell remoting enabled on client machines

param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string[]]$ClientIPs,
    [Parameter(Mandatory=$false)]
    [string]$Username = "Administrator"
)

$scriptBlock = {
    param($serverIP, $systemID)

    # Install Python if not present
    if (!(Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Installing Python..."
        # Download and install Python silently
        $pythonUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
        $installerPath = "$env:TEMP\python-installer.exe"
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
        Remove-Item $installerPath
    }

    # Install dependencies
    Write-Host "Installing monitoring dependencies..."
    python -m pip install psutil requests --quiet

    # Create monitoring agent
    Write-Host "Creating monitoring agent..."
    $agentCode = @"
import psutil
import requests
import time
from datetime import datetime

class SystemMonitor:
    def __init__(self, system_id, server_url):
        self.system_id = system_id
        self.server_url = server_url.rstrip('/')
        self.api_endpoint = f"{self.server_url}/api/systems/{system_id}/health"

    def get_system_health(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            status = "Online"
            health_status = "Healthy"
            if cpu_usage > 90 or memory_usage > 90 or disk_usage > 95:
                health_status = "Warning"
            return {
                'status': status,
                'health_status': health_status,
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'timestamp': datetime.now().isoformat()
            }
        except:
            return None

    def report_health(self):
        health_data = self.get_system_health()
        if not health_data:
            return False
        try:
            response = requests.post(self.api_endpoint, json=health_data, timeout=5)
            return response.status_code == 200
        except:
            return False

    def start_monitoring(self, interval=30):
        print(f"🚀 Starting monitoring for system {self.system_id}")
        print(f"📡 Server: {self.server_url}")
        print("-" * 50)
        while True:
            if self.report_health():
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Health reported")
            else:
                print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Report failed")
            time.sleep(interval)

if __name__ == "__main__":
    monitor = SystemMonitor($systemID, "http://$serverIP:5000")
    monitor.start_monitoring()
"@

    $agentCode | Out-File -FilePath "monitoring_agent.py" -Encoding UTF8

    # Create startup script
    Write-Host "Creating startup script..."
    $startupScript = @"
@echo off
python "C:\monitoring_agent.py"
"@

    $startupScript | Out-File -FilePath "start_monitoring.bat" -Encoding ASCII

    # Add to startup (optional)
    $startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    Copy-Item "start_monitoring.bat" $startupFolder

    Write-Host "✅ Deployment complete on $(hostname)"
    Write-Host "System ID: $systemID"
    Write-Host "Server: http://$serverIP:5000"
}

# Deploy to each client
for ($i = 0; $i -lt $ClientIPs.Count; $i++) {
    $clientIP = $ClientIPs[$i]
    $systemID = $i + 1  # Auto-assign system IDs starting from 1

    Write-Host "Deploying to $clientIP (System ID: $systemID)..."

    try {
        Invoke-Command -ComputerName $clientIP -Credential $Username -ScriptBlock $scriptBlock -ArgumentList $ServerIP, $systemID
        Write-Host "✅ Successfully deployed to $clientIP"
    } catch {
        Write-Host "❌ Failed to deploy to $clientIP : $($_.Exception.Message)"
    }
}

Write-Host "`n🎉 Network deployment complete!"
Write-Host "Check your Lab Control System dashboard to see connected clients."