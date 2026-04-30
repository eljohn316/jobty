from datetime import datetime
from typing import Literal, Sequence, Tuple

import rich
from pydantic import ValidationError
from rich.table import Table
from sqlalchemy import Row

from .constants import Colors
from .schemas import JobDetails, Status

JobRow = Tuple[
    int,
    datetime,
    str,
    str,
    Literal["Applied", "Interview", "Hired", "Rejected"],
    Literal["Onsite", "Hybrid", "Remote"],
]


def print_jobs(
    jobs: Sequence[Row[JobRow]],
):
    table = Table(box=rich.box.SIMPLE)

    table.add_column("ID", header_style=Colors.emerald.value)
    table.add_column("Role", header_style=Colors.emerald.value)
    table.add_column("Company", header_style=Colors.emerald.value)
    table.add_column(
        "Work arrangement", header_style=Colors.emerald.value, justify="center"
    )
    table.add_column("Status", header_style=Colors.emerald.value, justify="right")
    table.add_column("Added on", header_style=Colors.emerald.value, justify="right")

    for job_id, created_at, role, company, status, work_arrangement in jobs:
        table.add_row(
            f"[{Colors.gray.value}]{str(job_id)}",
            f"[bold]{role}",
            company,
            work_arrangement,
            render_status(status),
            f"[{Colors.gray.value}]{created_at.strftime('%b %-d, %Y - %I:%M %p')}",
        )

    rich.print(table)


def print_job(job_details_model: JobDetails):
    job = job_details_model.model_dump(exclude_none=True)

    table = Table(box=rich.box.SIMPLE, show_header=False)
    table.add_column(style=f"bold {Colors.emerald.value}")
    table.add_row("ID", str(job.get("id")))
    table.add_row("Role", f"[bold]{job.get('role')}")
    table.add_row("Company", job.get("company"))
    table.add_row("Location", job.get("location"))
    table.add_row("Work arrangement", job.get("work_arrangement"))
    table.add_row("Status", render_status(job.get("status")))
    table.add_row(
        "Source link",
        job.get("source_link", f"[{Colors.gray.value}]Unset"),
    )
    table.add_row(
        "Interview date",
        job.get("interview_date", f"[{Colors.gray.value}]Unset"),
    )
    table.add_row(
        "Interview time",
        job.get("interview_time", f"[{Colors.gray.value}]Unset"),
    )
    table.add_row(
        "Added on",
        job.get("created_at"),
    )
    rich.print(table)


def print_validation_errors(exception: ValidationError):
    rich.print()
    rich.print(f"[{Colors.red.value}]Validation error")
    for error in exception.errors():
        field: str = error["loc"][0]
        field = (" ".join(field.split("_"))).capitalize()
        message = error["msg"]
        rich.print(f"{field} - [{Colors.gray.value}]{message}")


def render_status(status: Status):
    if status == "Applied":
        return f"[yellow]{status}[/]"
    if status == "Interview":
        return f"[cyan]{status}[/]"
    if status == "Hired":
        return f"[green]{status}[/]"
    if status == "Rejected":
        return f"[red]{status}[/]"
