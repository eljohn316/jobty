from typing import Annotated

import typer

from .callback import (
    interview_date_callback,
    interview_time_callback,
    status_callback,
    work_arrangement_callback,
)
from .database import Base, engine
from .print_helpers import print_job, print_jobs
from .prompt import Prompt
from .schemas import JobUpdate
from .services import create_job, delete_job, get_job, get_jobs, update_job

Base.metadata.create_all(bind=engine)

app = typer.Typer(no_args_is_help=True)


@app.command("list")
def list(
    job_id: Annotated[
        int | None,
        typer.Argument(
            help="The ID of the Job to show",
            metavar="job_id",
        ),
    ] = None,
):
    """List all job application entries or a single job application entry if job id is provided."""
    if job_id:
        job = get_job(job_id)
        if job is None:
            typer.echo("Job application not found")
            return
        print_job(job)
    else:
        jobs = get_jobs()
        if len(jobs) == 0:
            typer.echo("You have no job applications yet.")
            return
        print_jobs(jobs)


@app.command("add")
def add():
    """
    Add job application entry.
    """
    prompt = Prompt()
    raw_answers = prompt.ask()
    answers = prompt.validate(raw_answers)
    create_job(answers)
    typer.echo()
    typer.echo("Job application added!")


@app.command()
def update(
    job_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the Job to update",
            metavar="job_id",
        ),
    ],
    role: Annotated[str | None, typer.Option(help="Job role")] = None,
    company: Annotated[str | None, typer.Option(help="Company name")] = None,
    location: Annotated[str | None, typer.Option(help="Location")] = None,
    work_arrangement: Annotated[
        str | None,
        typer.Option(help="Work arrangement", callback=work_arrangement_callback),
    ] = None,
    status: Annotated[
        str | None, typer.Option(help="Application status", callback=status_callback)
    ] = None,
    source_link: Annotated[str | None, typer.Option(help="Source link")] = None,
    interview_date: Annotated[
        str,
        typer.Option(
            help="Interview date (YYYY-MM-DD)", callback=interview_date_callback
        ),
    ] = "",
    interview_time: Annotated[
        str,
        typer.Option(
            help="Interview time (HH:MM AM/PM)", callback=interview_time_callback
        ),
    ] = "",
):
    """
    Update an existing job application entry.
    """
    if (
        role is None
        and company is None
        and location is None
        and work_arrangement is None
        and status is None
        and source_link is None
    ) and (interview_date == "" and interview_time == ""):
        typer.echo("No fields to update")
        return

    job_update = JobUpdate.model_validate(
        {
            "role": role,
            "company": company,
            "location": location,
            "work_arrangement": work_arrangement,
            "status": status,
            "source_link": source_link,
            "interview_date": interview_date,
            "interview_time": interview_time,
        }
    )

    updated_job_id = update_job(job_id, job_update)
    if updated_job_id is None:
        typer.echo("Job application not found")
        return

    typer.echo(f"Job #{updated_job_id} updated!")


@app.command()
def delete(job_id: int):
    """
    Delete an existing job application entry.
    """
    job = get_job(job_id)
    if job is None:
        typer.echo("Job application not found")
        return

    delete_job(job)
    typer.echo(f"Job #{job_id} deleted!")
