
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "syntra.db"


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                source_ip TEXT,
                destination_ip TEXT,
                protocol TEXT,
                signature TEXT,
                severity INTEGER,
                signature_id INTEGER
            )
        """)


def save_alert(alert):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            INSERT INTO alerts (
                timestamp,
                source_ip,
                destination_ip,
                protocol,
                signature,
                severity,
                signature_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            alert["timestamp"],
            alert["source_ip"],
            alert["destination_ip"],
            alert["protocol"],
            alert["signature"],
            alert["severity"],
            alert["signature_id"]
        ))
