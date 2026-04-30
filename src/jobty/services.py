import typer
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
            typer.echo("Job already exists")
            raise typer.Exit()


def get_job(job_id: int):
    with get_db_session() as session:
        query = select(models.Job).where(models.Job.id == job_id)
        job = session.execute(query).scalars().first()
        return job


def get_jobs(status: list[str], work_arrangement: list[str]):
    with get_db_session() as session:
        query = select(
            models.Job.id,
            models.Job.created_at,
            models.Job.role,
            models.Job.company,
            models.Job.status,
            models.Job.work_arrangement,
        )

        if status:
            query = query.where(models.Job.status.in_(status))

        if work_arrangement:
            query = query.where(models.Job.work_arrangement.in_(work_arrangement))

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
            typer.echo("Job application not found")
            raise typer.Exit()

        job_payload = job_update.model_dump(exclude_none=True)
        for field, value in job_payload.items():
            setattr(job, field, value)

        session.commit()
        session.refresh(job)

        return job.id
