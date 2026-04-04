import typer

from db import db_create_table
from forms import JobForm
from services import (
    get_all_job_applications,
    get_one_job_application,
    get_job_application_values,
    add_job_application,
    update_job_application,
    delete_job_application,
)

app = typer.Typer(no_args_is_help=True)


@app.command()
def list():
    """
    List all saved job application entries
    """
    get_all_job_applications()


@app.command()
def list_one(job_id: str):
    """
    List a single saved job application if exists
    """
    get_one_job_application(job_id)


@app.command()
def add():
    """
    Add a new job application entry
    """
    form = JobForm()
    job = form.ask_and_validate()
    add_job_application(job)


@app.command()
def update(job_id: str):
    """
    Update a job application entry
    """
    default_values = get_job_application_values(job_id)
    form = JobForm(default_values)
    job = form.ask_and_validate()
    update_job_application(job_id, job)


@app.command()
def delete(job_id: str):
    """
    Delete a job application entry
    """
    delete_job_application(job_id)


if __name__ == "__main__":
    db_create_table()
    app()
