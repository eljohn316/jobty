import rich

from schemas import Job
from db import db_insert_job
from constants import Colors


def add_job_application(job_model: Job):
    payload = job_model.model_dump()
    job_id = db_insert_job(payload)
    rich.print(f"[{Colors.emerald.value}]Successfully added")
    rich.print(job_id)
