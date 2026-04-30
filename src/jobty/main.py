from datetime import datetime
from typing import Annotated

import typer
from typer import Argument, Option

from .constants import Arrangement, Status
from .database import Base, engine
from .print_helpers import print_job, print_jobs
from .schemas import JobCreate, JobDetails, JobUpdate
from .services import create_job, delete_job, get_job, get_jobs, update_job
from .validations import validate_model

Base.metadata.create_all(bind=engine)

app = typer.Typer(no_args_is_help=True)


@app.command()
def list(
    job_id: Annotated[
        int,
        Argument(help="The ID of the Job to list", metavar="job_id"),
    ] = None,
):
    """List all job application entries or a single job application entry if job id is provided."""
    if job_id:
        job = get_job(job_id)
        if job is None:
            typer.echo("Job application not found")
            return
        job_details = JobDetails(**job.__dict__)
        print_job(job_details)
    else:
        jobs = get_jobs()
        if len(jobs) == 0:
            typer.echo("You have no job applications yet.")
            return
        print_jobs(jobs)


@app.command()
def add(
    role: Annotated[str, Option(help="Job role")],
    company: Annotated[str, Option(help="Company name")],
    location: Annotated[str, Option(help="Location")],
    work_arrangement: Annotated[Arrangement, Option(help="Work arrangement")],
    status: Annotated[Status, Option(help="Application status")] = "Applied",
    source_link: Annotated[str | None, Option(help="Source link")] = None,
    interview_date: Annotated[
        datetime | None,
        Option(
            help="Interview date",
            formats=["%m-%d-%Y"],
        ),
    ] = None,
    interview_time: Annotated[
        datetime | None,
        Option(
            help="Interview time",
            formats=["%I:%M %p"],
        ),
    ] = None,
):
    """
    Add job application entry.
    """
    job_create_model = validate_model(
        JobCreate,
        {
            "role": role,
            "company": company,
            "location": location,
            "work_arrangement": work_arrangement,
            "status": status,
            "source_link": source_link,
            "interview_date": interview_date.date() if interview_date else None,
            "interview_time": interview_time.time() if interview_time else None,
        },
    )
    create_job(job_create_model)
    typer.echo("Job application added")


@app.command()
def update(
    job_id: Annotated[
        int,
        Argument(help="The ID of the Job to update", metavar="job_id"),
    ],
    role: Annotated[str | None, Option(help="Job role")] = None,
    company: Annotated[str | None, Option(help="Company name")] = None,
    location: Annotated[str | None, Option(help="Location")] = None,
    work_arrangement: Annotated[
        Arrangement | None, Option(help="Work arrangement")
    ] = None,
    status: Annotated[Status | None, Option(help="Application status")] = None,
    source_link: Annotated[str | None, Option(help="Source link")] = None,
    interview_date: Annotated[
        datetime | None,
        Option(
            help="Interview date",
            formats=["%m-%d-%Y"],
        ),
    ] = None,
    interview_time: Annotated[
        datetime | None,
        Option(
            help="Interview time",
            formats=["%I:%M %p"],
        ),
    ] = None,
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
        and interview_date is None
        and interview_time is None
    ):
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
            "interview_date": interview_date.date() if interview_date else None,
            "interview_time": interview_time.time() if interview_time else None,
        }
    )

    updated_job_id = update_job(job_id, job_update)
    typer.echo(f"Job #{updated_job_id} updated")


@app.command()
def delete(
    job_id: Annotated[
        int,
        Argument(help="The ID of the Job to delete", metavar="job_id"),
    ],
):
    """
    Delete an existing job application entry.
    """
    job = get_job(job_id)
    if job is None:
        typer.echo("Job application not found")
        return

    delete_job(job)
    typer.echo(f"Job #{job_id} deleted")
