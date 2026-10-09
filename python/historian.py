import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tank_history.db"

def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tank_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                water_level REAL NOT NULL,
                pump_on INTEGER NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS pump_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                water_level REAL NOT NULL
            )
        """)

def log_reading(water_level, pump_on):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO tank_readings
                (timestamp, water_level, pump_on)
            VALUES (?, ?, ?)
            """,
            (
                datetime.now().isoformat(timespec="seconds"),
                water_level,
                int(pump_on)
            )
        )

def log_pump_event(event_type, water_level):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO pump_events
                (timestamp, event_type, water_level)
            VALUES (?, ?, ?)
            """,
            (
                datetime.now().isoformat(timespec="seconds"),
                event_type,
                water_level
            )
        )