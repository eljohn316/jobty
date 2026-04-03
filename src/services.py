import rich
from rich.table import Table

from schemas import Job
from db import db_insert_job, db_get_all_jobs, db_get_single_job
from constants import Colors
from utils import format_datetime


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

    table.add_column(f"[{Colors.emerald.value}]ID")
    table.add_column(f"[{Colors.emerald.value}]Role")
    table.add_column(f"[{Colors.emerald.value}]Date added")

    for job_id, role, date_added in jobs:
        table.add_row(job_id, role, format_datetime(date_added))

    rich.print(table)


def get_one_job_application(job_id: str):
    job = db_get_single_job(job_id)
    if job is None:
        rich.print("Job application not found")
        return

    (
        job_id,
        role,
        company_name,
        location,
        work_arrangement,
        status,
        job_posting_url,
        date_applied,
    ) = job

    table = Table(
        box=rich.box.HORIZONTALS,
        show_header=False,
    )
    table.add_row("[bold]Job application details")
    table.add_section()
    table.add_row(f"[bold {Colors.emerald.value}]ID", job_id)
    table.add_row(f"[bold {Colors.emerald.value}]Role", role)
    table.add_row(f"[bold {Colors.emerald.value}]Company name", company_name)
    table.add_row(f"[bold {Colors.emerald.value}]Location", location)
    table.add_row(f"[bold {Colors.emerald.value}]Work arrangement", work_arrangement)
    table.add_row(f"[bold {Colors.emerald.value}]Status", status)
    table.add_row(f"[bold {Colors.emerald.value}]Job posting URL", job_posting_url)
    table.add_row(
        f"[bold {Colors.emerald.value}]Date added", format_datetime(date_applied)
    )
    rich.print(table)
