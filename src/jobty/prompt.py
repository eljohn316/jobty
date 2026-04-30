from typing import Any

import questionary
import rich
import typer
from pydantic import ValidationError

from .constants import Arrangement, Colors, Status
from .print_helpers import print_validation_errors
from .schemas import JobCreate

styles = {
    "text": questionary.Style(
        [("question", "nobold"), ("answer", f"nobold fg:{Colors.amber.value}")]
    ),
    "select": questionary.Style(
        [
            ("question", "nobold"),
            ("answer", f"nobold fg:{Colors.amber.value}"),
            ("highlighted", f"fg:{Colors.amber.value}"),
            ("selected", f"fg:{Colors.amber.value}"),
        ]
    ),
}


class Prompt:
    def __init__(self, default_values: dict[str, Any] = {}):
        self.default_values = default_values

    def ask(self):
        rich.print("Fields with * are required.")
        rich.print()
        answers = questionary.prompt(self._questions)
        return answers

    def validate(self, answers: dict[str, Any]):
        try:
            validated_model = JobCreate.model_validate(answers)
            return validated_model
        except ValidationError as e:
            print_validation_errors(e)
            raise typer.Exit()

    @property
    def _questions(self):
        return [
            {
                "type": "text",
                "name": "role",
                "message": "* Role:",
                "default": self.default_values.get("role", ""),
                "style": styles["text"],
            },
            {
                "type": "text",
                "name": "company",
                "message": "* Company:",
                "default": self.default_values.get("company", ""),
                "style": styles["text"],
            },
            {
                "type": "text",
                "name": "location",
                "message": "* Location:",
                "default": self.default_values.get("location", ""),
                "style": styles["text"],
            },
            {
                "type": "select",
                "name": "work_arrangement",
                "message": "* Work arrangement",
                "default": self.default_values.get("work_arrangement", None),
                "choices": [
                    Arrangement.onsite.value,
                    Arrangement.remote.value,
                    Arrangement.hybrid.value,
                ],
                "style": styles["select"],
            },
            {
                "type": "select",
                "name": "status",
                "message": "* Status",
                "default": self.default_values.get("status", None),
                "choices": [
                    Status.applied.value,
                    Status.interview.value,
                    Status.hired.value,
                    Status.rejected.value,
                ],
                "style": styles["select"],
            },
            {
                "type": "text",
                "name": "source_link",
                "message": "Source link:",
                "default": self.default_values.get("source_link", ""),
                "style": styles["text"],
            },
            {
                "type": "text",
                "name": "interview_date",
                "message": "Interview date (YYYY-MM-DD):",
                "default": self.default_values.get("interview_date", ""),
                "style": styles["text"],
            },
            {
                "type": "text",
                "name": "interview_time",
                "message": "Interview time (HH:MM AM/PM):",
                "default": self.default_values.get("interview_time", ""),
                "style": styles["text"],
            },
        ]
