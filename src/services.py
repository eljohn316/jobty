from datetime import datetime
import rich
from rich.table import Table

from schemas import Job
from db import db_insert_job, db_get_all_jobs
from constants import Colors


def add_job_application(job_model: Job):
    payload = job_model.model_dump()
    job_id = db_insert_job(payload)
    rich.print(f"[{Colors.emerald.value}]Successfully added")
    rich.print(job_id)


def get_all_job_applications():
    jobs = db_get_all_jobs()
    if len(jobs) == 0:
        rich.print("You have no saved job applications")
        return

    table = Table(box=rich.box.SIMPLE)

    table.add_column("ID")
    table.add_column("Role")
    table.add_column("Date added")

    for job_id, role, date_added in jobs:
        table.add_row(
            job_id,
            role,
            datetime.fromisoformat(date_added).strftime("%b %-d, %Y - %I:%M:%S %p"),
        )

    rich.print(table)
