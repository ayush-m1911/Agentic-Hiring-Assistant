import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        resume_filename TEXT,
        match_score FLOAT,
        missing_skills TEXT,
        status TEXT,
        interview_start TIMESTAMP,
        interview_end TIMESTAMP,
        meet_link TEXT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
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

    now = datetime.utcnow()
    match_score = float(match_score)
    cursor.execute("""
    INSERT INTO candidates (
        name, email, resume_filename, match_score,
        missing_skills, status, created_at, updated_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (email) DO UPDATE SET
        match_score = EXCLUDED.match_score,
        missing_skills = EXCLUDED.missing_skills,
        status = EXCLUDED.status,
        updated_at = EXCLUDED.updated_at
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
        interview_start = %s,
        interview_end = %s,
        meet_link = %s,
        status = %s,
        updated_at = %s
    WHERE email = %s
    """, (
        interview_start,
        interview_end,
        meet_link,
        "INTERVIEW_SCHEDULED",
        datetime.utcnow(),
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
        status = %s,
        updated_at = %s
    WHERE email = %s
    """, (
        status,
        datetime.utcnow(),
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