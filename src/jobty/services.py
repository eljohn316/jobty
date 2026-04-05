from .schemas import Job
from .db import (
    db_insert_job,
    db_get_all_jobs,
    db_get_single_job,
    db_delete_job,
    db_update_job,
    db_create_table,
)


def init_job_applications_table():
    db_create_table()


def add_job_application(job_model: Job):
    payload = job_model.model_dump()
    job_id = db_insert_job(payload)
    return job_id


def get_all_job_applications():
    return db_get_all_jobs()


def get_one_job_application(job_id: str):
    return db_get_single_job(job_id)


def update_job_application(job_id, job: Job):
    payload = job.model_dump()
    db_update_job(job_id, payload)


def delete_job_application(job_id: str):
    db_delete_job(job_id)
