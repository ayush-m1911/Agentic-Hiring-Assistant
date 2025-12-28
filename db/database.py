import sqlite3
from datetime import datetime

DB_NAME = "hiring.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        resume_filename TEXT,
        match_score REAL,
        missing_skills TEXT,
        status TEXT,
        interview_start TEXT,
        interview_end TEXT,
        meet_link TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def upsert_candidate(
    name,
    email,
    resume_filename,
    match_score,
    missing_skills,
    status
):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT INTO candidates (
        name, email, resume_filename, match_score,
        missing_skills, status, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(email) DO UPDATE SET
        match_score = excluded.match_score,
        missing_skills = excluded.missing_skills,
        status = excluded.status,
        updated_at = excluded.updated_at
    """, (
        name,
        email,
        resume_filename,
        match_score,
        missing_skills,
        status,
        now,
        now
    ))

    conn.commit()
    conn.close()


def update_interview_details(
    email,
    interview_start,
    interview_end,
    meet_link
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE candidates
    SET
        interview_start = ?,
        interview_end = ?,
        meet_link = ?,
        status = ?,
        updated_at = ?
    WHERE email = ?
    """, (
        interview_start,
        interview_end,
        meet_link,
        "INTERVIEW_SCHEDULED",
        datetime.utcnow().isoformat(),
        email
    ))

    conn.commit()
    conn.close()


def update_final_status(email, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE candidates
    SET
        status = ?,
        updated_at = ?
    WHERE email = ?
    """, (
        status,
        datetime.utcnow().isoformat(),
        email
    ))

    conn.commit()
    conn.close()


def fetch_all_candidates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")
    rows = cursor.fetchall()

    conn.close()
    return rows