import sqlite3

def init_db():
    conn = sqlite3.connect('lab.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS systems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        status TEXT
    )
    ''')

    conn.commit()
    conn.close()