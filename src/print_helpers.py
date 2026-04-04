import rich
from rich.table import Table

from constants import Colors
from utils import format_datetime


def print_jobs_table(jobs):
    table = Table(box=rich.box.SIMPLE)

    table.add_column("ID", header_style=Colors.emerald.value)
    table.add_column("Role", header_style=Colors.emerald.value)
    table.add_column("Added on", header_style=Colors.emerald.value, justify="right")

    for job_id, role, date_added in jobs:
        table.add_row(job_id, role, format_datetime(date_added))

    rich.print(table)


def print_job_table(job):
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

    table = Table(box=rich.box.SIMPLE, show_header=False)
    table.add_column(style=f"bold {Colors.emerald.value}")
    table.add_row("ID", job_id)
    table.add_row("Role", role)
    table.add_row("Company name", company_name)
    table.add_row("Location", location)
    table.add_row("Work arrangement", work_arrangement)
    table.add_row("Status", status)
    table.add_row("Job posting URL", job_posting_url)
    table.add_row("Date added", format_datetime(date_applied))
    rich.print(table)
