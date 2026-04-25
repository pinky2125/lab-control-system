import sqlite3
from datetime import datetime

conn = sqlite3.connect('lab.db')
cursor = conn.cursor()

# SYSTEMS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS systems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    ip_address TEXT,
    mac_address TEXT,
    status TEXT DEFAULT 'Unknown',
    health_status TEXT DEFAULT 'Healthy',
    last_check_time TEXT,
    cpu_usage REAL,
    memory_usage REAL,
    disk_usage REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

# USERS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'User',
    is_active BOOLEAN DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT
)
''')

# AUDIT LOG TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    target_type TEXT,
    target_id INTEGER,
    details TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# SYSTEM HEALTH HISTORY TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS system_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id INTEGER NOT NULL,
    status TEXT,
    health_status TEXT,
    cpu_usage REAL,
    memory_usage REAL,
    disk_usage REAL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (system_id) REFERENCES systems(id) ON DELETE CASCADE
)
''')

conn.commit()
conn.close()

print("✅ Database initialized successfully with all tables!")