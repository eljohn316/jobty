from typing import Any

import typer
import questionary
import rich
from pydantic import ValidationError

from .schemas import Job
from .constants import Arrangement, Colors, Status


class JobForm:
    def __init__(self, default_values: dict[str, Any] = {}):
        self.default_values = default_values

    def ask(self):
        answers = questionary.prompt(self._questions)
        rich.print()
        return answers

    def validate(self, answers: dict[str, Any]):
        try:
            result = Job.model_validate(answers)
            return result
        except ValidationError as e:
            rich.print(f"[{Colors.red.value}]Validation error")
            for error in e.errors():
                field = to_pascal_case(error["loc"][0])
                message = error["msg"]
                rich.print(f"{field} - [{Colors.gray.value}]{message}")
            raise typer.Exit()

    def ask_and_validate(self):
        answers = self.ask()
        return self.validate(answers)

    @property
    def _questions(self):
        text_styles = questionary.Style(
            [
                ("question", "nobold"),
                ("answer", f"nobold fg:{Colors.amber.value}"),
            ]
        )
        select_styles = questionary.Style(
            [
                ("question", "nobold"),
                ("answer", f"nobold fg:{Colors.amber.value}"),
                ("highlighted", f"fg:{Colors.amber.value}"),
                ("selected", f"fg:{Colors.amber.value}"),
            ]
        )

        return [
            {
                "type": "text",
                "name": "role",
                "message": "Role:",
                "default": self.default_values.get("role", ""),
                "style": text_styles,
            },
            {
                "type": "text",
                "name": "company_name",
                "message": "Company name:",
                "default": self.default_values.get("company_name", ""),
                "style": text_styles,
            },
            {
                "type": "text",
                "name": "location",
                "message": "Location:",
                "default": self.default_values.get("location", ""),
                "style": text_styles,
            },
            {
                "type": "select",
                "name": "work_arrangement",
                "message": "Work arrangement",
                "default": self.default_values.get("work_arrangement", None),
                "choices": [
                    Arrangement.onsite.value,
                    Arrangement.remote.value,
                    Arrangement.hybrid.value,
                ],
                "style": select_styles,
            },
            {
                "type": "select",
                "name": "status",
                "message": "Status",
                "default": self.default_values.get("status", None),
                "choices": [
                    Status.applied.value,
                    Status.interview.value,
                    Status.hired.value,
                    Status.rejected.value,
                ],
                "style": select_styles,
            },
            {
                "type": "text",
                "name": "job_posting_url",
                "message": "Job posting URL:",
                "default": self.default_values.get("job_posting_url", ""),
                "style": text_styles,
            },
        ]


def to_pascal_case(text: str):
    return " ".join(text.split("_")).capitalize().replace("url", "URL")
