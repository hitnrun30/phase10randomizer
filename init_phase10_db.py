import os
import sqlite3
from datetime import datetime

# Database will live next to this script; adjust if you want it elsewhere
DB_PATH = os.path.join(os.path.dirname(__file__), "phase10_probs.sqlite")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        # Main probability table: one row per unique phase
        conn.execute("""
            CREATE TABLE IF NOT EXISTS phase_probability (
                phase_key    TEXT PRIMARY KEY,
                probability  REAL NOT NULL,
                trials       INTEGER NOT NULL,
                last_updated TEXT NOT NULL
            )
        """)

        # Breakdown table: one row per part per phase
        conn.execute("""
            CREATE TABLE IF NOT EXISTS phase_part (
                phase_key   TEXT NOT NULL,
                part_index  INTEGER NOT NULL,
                part_str    TEXT NOT NULL,
                part_type   TEXT,
                PRIMARY KEY (phase_key, part_index),
                FOREIGN KEY (phase_key) REFERENCES phase_probability(phase_key)
            )
        """)

        conn.commit()
        print(f"Database initialized at: {DB_PATH}")
        print("Tables 'phase_probability' and 'phase_part' are ready.")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
