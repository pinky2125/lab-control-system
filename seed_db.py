"""
Seed script to initialize default users and test systems
Run this after create_db.py
"""
import sqlite3
from datetime import datetime

def seed_database():
    conn = sqlite3.connect('lab.db')
    cursor = conn.cursor()

    # Check if users already exist
    existing_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    
    if existing_users == 0:
        # Add default admin user
        default_users = [
            ('admin', 'admin123', 'Admin'),
            ('manager', 'manager123', 'Manager'),
            ('user1', 'user123', 'User'),
        ]

        for name, password, role in default_users:
            try:
                cursor.execute(
                    "INSERT INTO users (name, password, role) VALUES (?, ?, ?)",
                    (name, password, role)
                )
                print(f"✅ Added user: {name} ({role})")
            except sqlite3.IntegrityError:
                print(f"⚠️ User {name} already exists")

    # Add some test systems
    existing_systems = cursor.execute("SELECT COUNT(*) FROM systems").fetchone()[0]
    
    if existing_systems == 0:
        test_systems = [
            ('PC-LAB-01', '192.168.1.101', 'AA:BB:CC:DD:EE:01', 'Online', 'Healthy'),
            ('PC-LAB-02', '192.168.1.102', 'AA:BB:CC:DD:EE:02', 'Online', 'Healthy'),
            ('PC-LAB-03', '192.168.1.103', 'AA:BB:CC:DD:EE:03', 'Offline', 'Unknown'),
            ('SERVER-01', '192.168.1.50', 'AA:BB:CC:DD:EE:50', 'Online', 'Healthy'),
        ]

        for name, ip, mac, status, health in test_systems:
            try:
                cursor.execute(
                    """INSERT INTO systems 
                       (name, ip_address, mac_address, status, health_status, last_check_time) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (name, ip, mac, status, health, datetime.now().isoformat())
                )
                print(f"✅ Added system: {name} ({ip})")
            except sqlite3.IntegrityError:
                print(f"⚠️ System {name} already exists")

    conn.commit()
    conn.close()
    print("\n✅ Database seeding complete!")
    print("\nDefault Credentials:")
    print("  - Username: admin, Password: admin123 (Admin)")
    print("  - Username: manager, Password: manager123 (Manager)")
    print("  - Username: user1, Password: user123 (User)")

if __name__ == "__main__":
    seed_database()
