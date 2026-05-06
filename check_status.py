#!/usr/bin/env python
"""
Monitor Status Checker
Shows current monitoring status from database
"""

import sqlite3
import time
from datetime import datetime

def check_monitoring_status():
    """Check and display current monitoring status"""
    try:
        conn = sqlite3.connect('lab.db')
        cursor = conn.cursor()

        # Get all systems with their latest status
        systems = cursor.execute('''
            SELECT
                s.id,
                s.name,
                s.status,
                s.health_status,
                s.cpu_usage,
                s.memory_usage,
                s.disk_usage,
                s.last_check_time
            FROM systems s
            ORDER BY s.id
        ''').fetchall()

        conn.close()

        print("\n" + "="*70)
        print("📊 LAB CONTROL SYSTEM - MONITORING STATUS")
        print("="*70)
        print(f"⏰ Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        print()

        if not systems:
            print("❌ No systems found in database")
            return

        for system in systems:
            system_id, name, status, health, cpu, mem, disk, last_check = system

            # Status indicators
            status_icon = "🟢" if status == "Online" else "🔴"
            health_icon = {
                "Healthy": "✅",
                "Warning": "⚠️",
                "Critical": "❌",
                None: "❓"
            }.get(health, "❓")

            print(f"{status_icon} System {system_id}: {name}")
            print(f"   Status: {status or 'Unknown'}")
            print(f"   Health: {health_icon} {health or 'Unknown'}")

            if cpu is not None:
                print(f"   CPU: {cpu:.1f}%")
            if mem is not None:
                print(f"   Memory: {mem:.1f}%")
            if disk is not None:
                print(f"   Disk: {disk:.1f}%")

            if last_check:
                print(f"   Last Check: {last_check}")
            else:
                print("   Last Check: Never")

            print()

        # Summary
        online_count = sum(1 for s in systems if s[2] == "Online")
        healthy_count = sum(1 for s in systems if s[3] == "Healthy")

        print(f"📈 Summary: {online_count}/{len(systems)} systems online, {healthy_count} healthy")
        print("="*70)

    except Exception as e:
        print(f"❌ Error checking status: {e}")

def main():
    print("🔍 Monitoring Status Checker")
    print("Press Ctrl+C to stop")
    print()

    try:
        while True:
            check_monitoring_status()
            time.sleep(10)  # Update every 10 seconds
    except KeyboardInterrupt:
        print("\n⏹️ Status checker stopped")

if __name__ == "__main__":
    main()