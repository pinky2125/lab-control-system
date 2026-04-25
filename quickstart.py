#!/usr/bin/env python
"""
Quick Start Script for Lab Control System
This script automates the setup process
"""

import os
import subprocess
import sys

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
    """Main setup function"""
    print("\n")
    print("🧪" * 30)
    print("  LAB CONTROL SYSTEM - QUICK START")
    print("🧪" * 30)
    print("\n")

    # Check if already in venv
    if sys.prefix == sys.base_prefix:
        print("⚠️  Not in virtual environment")
        print("📝 Please activate venv first:")
        print("   Windows: venv\\Scripts\\activate")
        print("   Linux/Mac: source venv/bin/activate")
        return

    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return

    # Step 2: Create database
    if not run_command("python create_db.py", "Creating database tables"):
        return

    # Step 3: Seed database
    if not run_command("python seed_db.py", "Seeding default users and systems"):
        return

    # Print completion message
    print("\n")
    print("✨" * 30)
    print("\n🎉 SETUP COMPLETE!\n")
    print("✨" * 30)
    print("""
    Next steps:

    1. Start the server:
       python run.py

    2. Access the application:
       http://localhost:5000

    3. Login with:
       Username: admin
       Password: admin123

    4. (Optional) Run monitoring agent on another terminal:
       python monitoring_agent.py --system-id 1 --server http://localhost:5000

    📚 For more information, see:
       - README.md (Features and setup)
       - IMPLEMENTATION_GUIDE.md (Detailed guide and next steps)

    🚀 Happy monitoring!
    """)

if __name__ == "__main__":
    main()
