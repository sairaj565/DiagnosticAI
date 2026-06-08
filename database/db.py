import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'diagnostic.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        name           TEXT NOT NULL,
        email          TEXT UNIQUE NOT NULL,
        password       TEXT NOT NULL,
        hospital       TEXT,
        specialization TEXT,
        phone          TEXT,
        license        TEXT,
        created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id  TEXT,
        name        TEXT,
        age         INTEGER,
        gender      TEXT,
        smoking     TEXT,
        phone       TEXT,
        notes       TEXT,
        scan_type   TEXT,
        image_path  TEXT,
        result      TEXT,
        confidence  REAL,
        doctor      TEXT,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reset_tokens (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        email      TEXT NOT NULL,
        token      TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_profiles (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id     TEXT UNIQUE NOT NULL,
        name       TEXT NOT NULL,
        gender     TEXT,
        phone      TEXT,
        doctor     TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()

    existing_cols = [row[1] for row in cursor.execute("PRAGMA table_info(patients)").fetchall()]

    migrations = [
        ("pack_years",       "REAL DEFAULT 0"),
        ("symptoms",         "TEXT DEFAULT ''"),
        ("smoking_type",     "TEXT DEFAULT ''"),
        ("amount_per_day",   "REAL DEFAULT 0"),
        ("years_smoked",     "REAL DEFAULT 0"),
        ("years_since_quit", "REAL DEFAULT 0"),
        ("profile_ref_id",   "TEXT DEFAULT ''"),
    ]

    for col_name, col_def in migrations:
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE patients ADD COLUMN {col_name} {col_def}")
            print(f"Migration: added column '{col_name}'")

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
    