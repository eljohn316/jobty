from datetime import datetime

import typer


def work_arrangement_callback(value: str):
    if value is not None and value not in ["Onsite", "Hybrid", "Remote"]:
        raise typer.BadParameter(
            'Invalid value. Allowed values: "Onsite", "Hybrid", "Remote"'
        )
    return value


def status_callback(value: str):
    if value is not None and value not in ["Applied", "Interview", "Hired", "Rejected"]:
        raise typer.BadParameter(
            'Invalid value. Allowed values: "Applied", "Interview", "Hired", "Rejected"'
        )
    return value


def interview_date_callback(value: str):
    try:
        if value != "" and datetime.strptime(value, "%Y-%m-%d").date():
            return value
        return value
    except ValueError:
        raise typer.BadParameter(
            'Interview date should exactly be this format "YYYY-MM-DD"'
        )


def interview_time_callback(value: str):
    try:
        if value != "" and datetime.strptime(value, "%I:%M %p").time():
            return value
        return value
    except ValueError:
        raise typer.BadParameter(
            'Interview time should exactly be this format "HH:MM AM/PM"'
        )
