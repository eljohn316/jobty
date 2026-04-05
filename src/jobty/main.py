import rich
import typer

from .db import db_create_table
from .forms import JobForm
from .services import (
    get_all_job_applications,
    get_one_job_application,
    add_job_application,
    update_job_application,
    delete_job_application,
)
from .print_helpers import print_jobs_table, print_job_table

app = typer.Typer(no_args_is_help=True)
db_create_table()


@app.command()
def list():
    """
    List all saved job application entries
    """
    jobs = get_all_job_applications()
    if len(jobs) == 0:
        rich.print("No job applications yet")
        return

    print_jobs_table(jobs)


@app.command()
def list_one(job_id: str):
    """
    List a single saved job application if exists
    """
    job = get_one_job_application(job_id)
    if job is None:
        rich.print("Job application not found")
        return

    print_job_table(job)


@app.command()
def add():
    """
    Add a new job application entry
    """
    form = JobForm()
    job_model = form.ask_and_validate()
    job_id = add_job_application(job_model)
    rich.print(job_id)


@app.command()
def update(job_id: str):
    """
    Update a job application entry
    """
    job = get_one_job_application(job_id)
    if job is None:
        rich.print("Job application not found")
        return

    default_values = {
        "role": job[1],
        "company_name": job[2],
        "location": job[3],
        "work_arrangement": job[4],
        "status": job[5],
        "job_posting_url": job[6],
    }

    form = JobForm(default_values)
    job_model = form.ask_and_validate()
    update_job_application(job_id, job_model)

    rich.print(job_id)


@app.command()
def delete(job_id: str):
    """
    Delete a job application entry
    """
    job = get_one_job_application(job_id)
    if job is None:
        rich.print("Job application not found")
        return

    delete_job_application(job_id)
    rich.print(job_id)
