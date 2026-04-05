from datetime import datetime


def format_datetime(date_string):
    return datetime.fromisoformat(date_string).strftime("%b %-d, %Y - %I:%M:%S %p")
