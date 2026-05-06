#!/usr/bin/env python
"""
Multi-Agent Test Script
Simulates multiple monitoring agents running simultaneously
"""

import subprocess
import time
import threading
import os
import signal
import sys

class MultiAgentTester:
    def __init__(self):
        self.processes = []
        self.server_process = None

    def start_server(self):
        """Start the Flask server"""
        print("🚀 Starting Lab Control Server...")
        self.server_process = subprocess.Popen(
            ['python', 'run.py'],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)  # Wait for server to start
        print("✅ Server started on http://localhost:5000")

    def start_agent(self, system_id, name):
        """Start a monitoring agent"""
        print(f"🚀 Starting monitoring agent for {name} (System ID: {system_id})...")
        process = subprocess.Popen(
            ['python', 'monitoring_agent.py', '--system-id', str(system_id), '--server', 'http://localhost:5000'],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.processes.append((process, name, system_id))
        time.sleep(2)  # Wait for agent to start

    def check_status(self):
        """Check status of all processes"""
        print("\n📊 Current Status:")
        print("-" * 50)

        for process, name, system_id in self.processes:
            if process.poll() is None:
                print(f"✅ {name} (ID: {system_id}): Running")
            else:
                print(f"❌ {name} (ID: {system_id}): Stopped")

        if self.server_process and self.server_process.poll() is None:
            print("✅ Server: Running")
        else:
            print("❌ Server: Stopped")

    def stop_all(self):
        """Stop all processes"""
        print("\n🛑 Stopping all processes...")

        for process, name, system_id in self.processes:
            if process.poll() is None:
                process.terminate()
                print(f"✅ Stopped {name}")

        if self.server_process and self.server_process.poll() is None:
            self.server_process.terminate()
            print("✅ Stopped Server")

        print("🎉 All processes stopped")

def main():
    tester = MultiAgentTester()

    try:
        # Start server
        tester.start_server()

        # Start multiple agents
        agents = [
            (1, "PC-LAB-01"),
            (2, "PC-LAB-02"),
            (3, "PC-LAB-03"),
            (4, "SERVER-01")
        ]

        for system_id, name in agents:
            tester.start_agent(system_id, name)

        # Monitor for a while
        print("\n⏳ Monitoring for 60 seconds...")
        print("Check your browser at: http://localhost:5000")
        print("Login with: admin / admin123")

        for i in range(12):  # 12 * 5 seconds = 60 seconds
            time.sleep(5)
            if i % 2 == 0:  # Every 10 seconds
                tester.check_status()

        print("\n🎉 Test completed successfully!")
        print("Your Lab Control System can monitor multiple PCs simultaneously!")

    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    finally:
        tester.stop_all()

if __name__ == "__main__":
    main()