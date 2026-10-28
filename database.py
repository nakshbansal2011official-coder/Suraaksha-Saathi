import sqlite3
import os
import json
from datetime import datetime, timezone, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "surakshaa_saathi.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_ist_now():
    # India Standard Time (UTC+5:30)
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist)

def get_ist_date_str():
    return get_ist_now().strftime("%Y-%m-%d")

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        country TEXT NOT NULL,
        state TEXT NOT NULL,
        city TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        preferred_lang TEXT DEFAULT 'hi',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        participant_id INTEGER NOT NULL,
        quiz_date TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_marks INTEGER NOT NULL,
        answers_json TEXT NOT NULL,
        certificate_id TEXT,
        submitted_at TEXT NOT NULL,
        UNIQUE(participant_id, quiz_date),
        FOREIGN KEY(participant_id) REFERENCES participants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        certificate_number TEXT UNIQUE NOT NULL,
        participant_id INTEGER NOT NULL,
        participant_name TEXT NOT NULL,
        quiz_date TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_marks INTEGER NOT NULL,
        certificate_type TEXT NOT NULL,
        issue_date TEXT NOT NULL,
        email_status TEXT DEFAULT 'Queued',
        delivery_log TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(participant_id) REFERENCES participants(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS scam_scenarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scenario_id TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        risk_level TEXT NOT NULL,
        target_audience TEXT NOT NULL,
        situation TEXT NOT NULL,
        how_works TEXT NOT NULL,
        warning_signs TEXT NOT NULL,
        manipulation TEXT NOT NULL,
        victim_actions TEXT NOT NULL,
        avoid_actions TEXT NOT NULL,
        risk_reduction TEXT NOT NULL,
        reporting_guidance TEXT NOT NULL,
        last_reviewed TEXT NOT NULL,
        tags TEXT NOT NULL,
        published INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        profession TEXT NOT NULL,
        rating INTEGER NOT NULL,
        review_text TEXT NOT NULL,
        status TEXT DEFAULT 'approved',
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS posters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        image_url TEXT NOT NULL,
        source_refs TEXT NOT NULL,
        published INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS daily_tips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        tip_text TEXT NOT NULL,
        explanation TEXT NOT NULL,
        related_topic TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS admin_config (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        details TEXT,
        ip_address TEXT,
        timestamp TEXT NOT NULL
    );
    ''')

    # Default admin config (passcode hash or token)
    # Default admin credentials: username 'admin', pass 'Surakshaa@2026'
    cursor.execute("SELECT value FROM admin_config WHERE key = 'admin_password_hash'")
    if not cursor.fetchone():
        # Store simple SHA256 hashed password for standard setup
        import hashlib
        default_hash = hashlib.sha256("Surakshaa@2026".encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO admin_config (key, value) VALUES ('admin_password_hash', ?)", (default_hash,))
        cursor.execute("INSERT INTO admin_config (key, value) VALUES ('ai_model', ?)", ("gpt-4o-mini",))
        cursor.execute("INSERT INTO admin_config (key, value) VALUES ('system_status', ?)", ("operational",))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)

