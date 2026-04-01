import typer

from forms import add_job_form
from services import add_job_application

app = typer.Typer(no_args_is_help=True)


@app.command()
def list():
    """
    List all saved job application entries
    """
    print("Job applications")


@app.command()
def add():
    """
    Add a new job application entry
    """
    payload = add_job_form()
    add_job_application(payload)


@app.command()
def update(job_id: str):
    """
    Update a job application entry
    """
    print(f"Update job application {job_id}")


@app.command()
def delete(job_id: str):
    """
    Delete a job application entry
    """
    print(f"Delete job application entry {job_id}")


if __name__ == "__main__":
    app()
