import sqlite3
import uuid
from contextlib import contextmanager
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
                UNIQUE(role, company_name)
            ); 
        """
        curr.execute(query)


def db_insert_job(data: dict[str, Any]):
    try:
        with db_get_connection() as conn:
            curr = conn.cursor()
            job_id = uuid.uuid4().hex

            insert_query = """
                INSERT INTO jobs (
                    id, role, company_name, location, work_arrangement, status, job_posting_url
                ) VALUES (
                    :id, :role, :company_name, :location, :work_arrangement, :status, :job_posting_url
                );
            """
            curr.execute(insert_query, {"id": job_id, **data})
            return job_id
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            rich.print(f"[{Colors.red.value}]Job already exists")
        raise typer.Exit()
