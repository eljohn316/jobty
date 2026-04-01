import rich
from rich.padding import Padding

from schemas import Job


def add_job_application(payload: Job):
    job_id = Padding(payload.id_, (1, 0, 0, 0))
    rich.print(job_id)
