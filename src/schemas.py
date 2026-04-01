from uuid import uuid4
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_serializer


class Status(Enum):
    applied = "Applied"
    interview = "Interview"
    hired = "Hired"
    rejected = "Rejected"
    ghosted = "Ghosted"


class Arrangement(Enum):
    onsite = "Onsite"
    hybrid = "Hybrid"
    remote = "Remote"


class Job(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        str_min_length=1,
        validate_default=True,
        validate_assignment=True,
        use_enum_values=True,
    )

    id_: str = Field(alias="id", default_factory=lambda: uuid4().hex)
    role: str
    company_name: str
    company_location: str
    work_arrangement: Arrangement
    status: Status = Field(
        default=Status.applied.value,
    )
    job_posting_url: HttpUrl | None = None
    interview_date: date | None = None
    date_applied: datetime = Field(default_factory=datetime.now)
    resume: str | None = None
    cover_letter: str | None = None
