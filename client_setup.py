#!/usr/bin/env python
"""
Client Setup Script for Lab Control System
Run this on each client PC to set up monitoring
"""

import os
import subprocess
import sys
import platform

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, capture_output=False)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main client setup function"""
    print("\n")
    print("🖥️" * 30)
    print("  CLIENT MONITORING SETUP")
    print("🖥️" * 30)
    print("\n")

    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ required")
        return

    print(f"✅ Python {sys.version.split()[0]} detected")

    # Install psutil
    if not run_command("pip install psutil requests", "Installing monitoring dependencies"):
        return

    print("\n")
    print("✨" * 30)
    print("\n🎉 CLIENT SETUP COMPLETE!\n")
    print("✨" * 30)
    print("""
    Next steps:

    1. Copy monitoring_agent.py to this machine
    2. Get your System ID from the Lab Control Server
    3. Run the monitoring agent:

       python monitoring_agent.py --system-id YOUR_ID --server http://SERVER_IP:5000

    Example:
       python monitoring_agent.py --system-id 2 --server http://192.168.1.100:5000

    📚 The agent will monitor CPU, Memory, and Disk usage
    📡 And report back to your Lab Control Server every 30 seconds

    🚀 Happy monitoring!
    """)

if __name__ == "__main__":
    main()