import sqlite3

dbFile = "vault.db"

def init_db():
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password BLOB NOT NULL
            )
        """)
        conn.commit()

def saveEntry(service, username, encrypted_password):
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO passwords (service, username, password)
            VALUES (?, ?, ?)
        """, (service, username, encrypted_password))
        conn.commit()

def getEntries():
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT service, username, password FROM passwords")
        return cursor.fetchall()