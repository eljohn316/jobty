from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from . import models
from .database import get_db_session
from .schemas import JobCreate, JobUpdate


def create_job(job: JobCreate):
    with get_db_session() as session:
        try:
            new_job = models.Job(
                role=job.role,
                company=job.company,
                location=job.location,
                work_arrangement=job.work_arrangement,
                status=job.status,
                source_link=job.source_link,
                interview_date=job.interview_date,
                interview_time=job.interview_time,
            )
            session.add(new_job)
            session.commit()
            session.refresh(new_job)
            return new_job
        except IntegrityError:
            return None


def get_job(job_id: int):
    with get_db_session() as session:
        job = session.get(models.Job, job_id)
        return job


def get_jobs():
    with get_db_session() as session:
        query = select(
            models.Job.id,
            models.Job.created_at,
            models.Job.role,
            models.Job.company,
            models.Job.status,
        ).order_by(models.Job.created_at.desc())
        jobs = session.execute(query).all()
        return jobs


def delete_job(job: models.Job):
    with get_db_session() as session:
        session.delete(job)
        session.commit()


def update_job(job_id: int, job_update: JobUpdate):
    with get_db_session() as session:
        job = session.get(models.Job, job_id)
        if job is None:
            return None

        job_payload = job_update.model_dump(exclude_none=True)
        for field, value in job_payload.items():
            setattr(job, field, value)

        session.commit()
        session.refresh(job)

        return job.id
