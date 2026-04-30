from typing import Any

import typer
from pydantic import BaseModel, ValidationError

from .print_helpers import print_validation_errors


def validate_model(model: type[BaseModel], payload: dict[str, Any]):
    try:
        validated_model = model.model_validate(payload)
        return validated_model
    except ValidationError as e:
        print_validation_errors(e)
        raise typer.Exit()
