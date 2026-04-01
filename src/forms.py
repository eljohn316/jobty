from typing import Any

import typer
import questionary
import rich
from rich.padding import Padding
from pydantic import ValidationError

from schemas import Job
from constants import Colors

ARRANGEMENT = ["Onsite", "Remote", "Hybrid"]


def text_field(message: str, default="", validate: Any = None):
    return questionary.text(
        message,
        default=default,
        style=questionary.Style(
            [
                ("question", "nobold"),
                ("answer", f"nobold fg:{Colors.sky_blue.value}"),
            ]
        ),
        validate=validate,
    )


def select_field(message: str, choices: list[str], default: str | None = None):
    return questionary.select(
        message,
        choices=choices,
        default=default,
        style=questionary.Style(
            [
                ("question", "nobold"),
                ("answer", f"nobold fg:{Colors.sky_blue.value}"),
                ("highlighted", f"fg:{Colors.sky_blue.value}"),
                ("selected", f"fg:{Colors.sky_blue.value}"),
            ]
        ),
    )


def add_job_form():
    try:
        rich.print(f"[bold {Colors.emerald.value}] Fill in the fields below")
        answers = questionary.form(
            role=text_field("Role:"),
            company_name=text_field("Company name:"),
            company_location=text_field("Company location:"),
            work_arrangement=select_field("Work arrangement:", choices=ARRANGEMENT),
            job_posting_url=text_field("Job posting URL:"),
        ).ask()
        result = Job.model_validate(answers)
        return result
    except ValidationError as e:
        error_heading = Padding(
            "Validation error", (1, 0, 0, 0), style=f"bold {Colors.red.value}"
        )
        rich.print(error_heading)
        for error in e.errors():
            field = to_pascal_case(error["loc"][0])
            message = error["msg"]
            rich.print(f"{field} - [{Colors.sky_blue.value}]{message}")
        raise typer.Exit()


def to_pascal_case(text: str):
    return " ".join(text.split("_")).capitalize().replace("url", "URL")
