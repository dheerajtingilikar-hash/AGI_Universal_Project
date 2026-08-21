import sqlite3
import json
import time
import os

class Memory:
    def __init__(self, db_path="Brain_Data/collection/mem0/storage.sqlite"):
        print("🧠 Initializing Memory System...")

        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            timestamp REAL
        )
        """)

        self.conn.commit()
        print(" Memory Ready")

    # Store conversation
    def store(self, role, content):
        self.cursor.execute(
            "INSERT INTO memory (role, content, timestamp) VALUES (?, ?, ?)",
            (role, content, time.time())
        )
        self.conn.commit()

    # Get last N memories
    def recall(self, limit=10):
        self.cursor.execute(
            "SELECT role, content FROM memory ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = self.cursor.fetchall()

        return [
            {"role": r[0], "content": r[1]}
            for r in reversed(rows)
        ]

    # Clear memory
    def clear(self):
        self.cursor.execute("DELETE FROM memory")
        self.conn.commit()