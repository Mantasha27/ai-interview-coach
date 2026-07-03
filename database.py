import sqlite3

def init_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        username TEXT,
        domain TEXT,
        score REAL,
        percentage REAL,
        confidence REAL
    )
    """)

    conn.commit()
    return conn, cursor