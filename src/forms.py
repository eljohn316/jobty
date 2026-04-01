from typing import Any

import typer
import questionary
import rich
from pydantic import ValidationError

from schemas import Job

ARRANGEMENT = ["Onsite", "Remote", "Hybrid"]


def text_field(message: str, default="", validate: Any = None):
    return questionary.text(
        message,
        default=default,
        style=questionary.Style([("answer", "fg:#0ea5e9")]),
        validate=validate,
    )


def select_field(message: str, choices: list[str], default: str | None = None):
    return questionary.select(
        message,
        choices=choices,
        default=default,
        style=questionary.Style([("answer", "fg:#0ea5e9"), ("selected", "fg:#0ea5e9")]),
    )


def add_job_form():
    try:
        answers = questionary.form(
            role=text_field("Role:"),
            company_name=text_field("Company name:"),
            company_location=text_field("Company location:"),
            work_arrangement=select_field("Work arrangement:", choices=ARRANGEMENT),
            job_posting_url=text_field("Job posting URL:"),
        ).ask()
        result = Job.model_validate(answers).model_dump()
        return result
    except ValidationError as e:
        print()
        rich.print("[bold red]Validation Error")
        for error in e.errors():
            field = to_pascal_case(error["loc"][0])
            message = error["msg"]
            rich.print(f"[bold]{field}[/bold] - {message}")
        raise typer.Exit()


def to_pascal_case(text: str):
    return " ".join(text.split("_")).capitalize().replace("url", "URL")
