"""
System Monitoring Agent
Run this script on each client PC to monitor and report system health to the Lab Control System

Usage: python monitoring_agent.py --system-id 1 --server http://localhost:5000

This agent will:
- Monitor CPU, Memory, and Disk usage
- Check if system is online
- Report status to the Lab Control Server every 30 seconds
"""

import psutil
import requests
import socket
import argparse
import time
import json
from datetime import datetime

class SystemMonitor:
    def __init__(self, system_id, server_url):
        self.system_id = system_id
        self.server_url = server_url.rstrip('/')
        self.api_endpoint = f"{self.server_url}/api/systems/{system_id}/health"

    def get_system_health(self):
        """Get current system health metrics"""
        try:
            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)

            # Get Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent

            # Get Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent

            # Determine status
            status = "Online"
            health_status = "Healthy"

            # Health checks
            if cpu_usage > 90:
                health_status = "Warning"
            if memory_usage > 90:
                health_status = "Warning"
            if disk_usage > 95:
                health_status = "Warning"

            return {
                'status': status,
                'health_status': health_status,
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error getting system health: {e}")
            return None

    def report_health(self):
        """Report system health to the server"""
        try:
            health_data = self.get_system_health()
            if not health_data:
                return False

            response = requests.post(
                self.api_endpoint,
                json=health_data,
                timeout=5
            )

            if response.status_code == 200:
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Health reported - "
                      f"CPU: {health_data['cpu_usage']:.1f}%, "
                      f"Memory: {health_data['memory_usage']:.1f}%, "
                      f"Disk: {health_data['disk_usage']:.1f}%")
                return True
            else:
                print(f"❌ Server error: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Cannot connect to server: {self.server_url}")
            return False
        except Exception as e:
            print(f"❌ Error reporting health: {e}")
            return False

    def start_monitoring(self, interval=30):
        """Start continuous monitoring"""
        print(f"🚀 Starting monitoring for system {self.system_id}")
        print(f"📡 Server URL: {self.server_url}")
        print(f"⏱️  Report interval: {interval} seconds")
        print("-" * 60)

        try:
            while True:
                self.report_health()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n⏹️ Monitoring stopped by user")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="System Monitoring Agent for Lab Control System"
    )
    parser.add_argument('--system-id', type=int, required=True, help='System ID in database')
    parser.add_argument('--server', required=True, help='Lab Control Server URL (e.g., http://localhost:5000)')
    parser.add_argument('--interval', type=int, default=30, help='Report interval in seconds')

    args = parser.parse_args()

    monitor = SystemMonitor(args.system_id, args.server)
    monitor.start_monitoring(args.interval)
