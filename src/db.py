import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime
from typing import Any

import rich
import typer

from constants import Colors


@contextmanager
def db_get_connection():
    conn = sqlite3.connect("jobs.db")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def db_create_table():
    with db_get_connection() as conn:
        curr = conn.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS jobs(
                id TEXT PRIMARY KEY NOT NULL,
                role TEXT NOT NULL,
                company_name TEXT NOT NULL,
                location TEXT NOT NULL,
                work_arrangement TEXT NOT NULL,
                status TEXT NOT NULL,
                job_posting_url TEXT NOT NULL,
                date_added TEXT,
                UNIQUE(role, company_name)
            ) STRICT; 
        """
        curr.execute(query)


def db_get_all_jobs():
    with db_get_connection() as conn:
        curr = conn.cursor()
        query = "SELECT id, role, date_added FROM jobs;"
        rows = curr.execute(query).fetchall()
        return rows


def db_insert_job(data: dict[str, Any]):
    try:
        with db_get_connection() as conn:
            curr = conn.cursor()
            job_id = uuid.uuid4().hex

            insert_query = """
                INSERT INTO jobs (
                    id, role, company_name, location, work_arrangement, status, job_posting_url, date_added
                ) VALUES (
                    :id, :role, :company_name, :location, :work_arrangement, :status, :job_posting_url, :date_added
                );
            """
            curr.execute(
                insert_query, {"id": job_id, **data, "date_added": datetime.now()}
            )
            return job_id
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            rich.print(f"[{Colors.red.value}]Job already exists")
        raise typer.Exit()


def db_get_single_job(job_id: str):
    with db_get_connection() as conn:
        curr = conn.cursor()
        query = "SELECT * FROM jobs WHERE id = ?;"
        row = curr.execute(query, (job_id,)).fetchone()
        return row


def db_update_job(job_id, data: dict[str, Any]):
    with db_get_connection() as conn:
        curr = conn.cursor()
        query = """
            UPDATE jobs
            SET role = :role,
                company_name = :company_name,
                location = :location,
                work_arrangement = :work_arrangement,
                status = :status,
                job_posting_url = :job_posting_url
            WHERE id = :id
        """
        curr.execute(query, {**data, "id": job_id})


def db_delete_job(job_id: str):
    with db_get_connection() as conn:
        curr = conn.cursor()
        query = "DELETE FROM jobs WHERE id = ?;"
        curr.execute(query, (job_id,))
