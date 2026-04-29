from datetime import datetime
from typing import Literal, Sequence, Tuple

import rich
from rich.table import Table
from sqlalchemy import Row

from .constants import Colors
from .models import Job

JobRow = Tuple[
    int,
    datetime,
    str,
    str,
    Literal["Applied", "Interview", "Hired", "Rejected"],
]


def print_jobs(
    jobs: Sequence[Row[JobRow]],
):
    table = Table(box=rich.box.SIMPLE)

    table.add_column("ID", header_style=Colors.emerald.value)
    table.add_column("Role", header_style=Colors.emerald.value)
    table.add_column("Company", header_style=Colors.emerald.value)
    table.add_column("Status", header_style=Colors.emerald.value, justify="right")
    table.add_column("Added on", header_style=Colors.emerald.value, justify="right")

    for job_id, created_at, role, company, status in jobs:
        table.add_row(
            str(job_id),
            role,
            company,
            status,
            created_at.strftime("%b %-d, %Y - %I:%M %p"),
        )

    rich.print(table)


def print_job(job: Job):

    table = Table(box=rich.box.SIMPLE, show_header=False)
    table.add_column(style=f"bold {Colors.emerald.value}")
    table.add_row("ID", str(job.id))
    table.add_row("Role", job.role)
    table.add_row("Company", job.company)
    table.add_row("Location", job.location)
    table.add_row("Work arrangement", job.work_arrangement)
    table.add_row("Status", job.status)
    table.add_row(
        "Source link",
        job.source_link if job.source_link else f"[{Colors.gray.value}]Unset",
    )
    table.add_row(
        "Interview date",
        job.interview_date.strftime("%b %d, %Y")
        if job.interview_date
        else f"[{Colors.gray.value}]Unset",
    )
    table.add_row(
        "Interview time",
        job.interview_time.strftime("%I:%M %p")
        if job.interview_time
        else f"[{Colors.gray.value}]Unset",
    )
    rich.print(table)
