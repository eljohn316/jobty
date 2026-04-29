from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from .constants import Arrangement, Status


class JobBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        str_min_length=1,
        validate_default=True,
        use_enum_values=True,
    )


class JobBase(JobBaseModel):
    role: str
    company: str
    location: str
    work_arrangement: Arrangement
    status: Status = Field(default=Status.applied)
    source_link: str | None = None
    interview_date: date | None = None
    interview_time: time | None = None

    @field_validator("source_link", "interview_date", "interview_time", mode="before")
    @classmethod
    def ensure_none(cls, value: str | None):
        if isinstance(value, str) and len(value) == 0:
            return None
        return value

    @field_validator("interview_time", mode="before")
    @classmethod
    def ensure_time(cls, value: str):
        if isinstance(value, str) and len(value) > 0:
            return datetime.strptime(value, "%I:%M %p").time()
        return value

    @field_serializer("interview_date", mode="plain")
    def ser_interview_date(self, value: date | None):
        if isinstance(value, date):
            return value.strftime("%b %d, %Y")
        return value

    @field_serializer("interview_time", mode="plain")
    def ser_interview_time(self, value: time | None):
        if isinstance(value, time):
            return value.strftime("%I:%M %p")
        return value


class JobCreate(JobBase):
    pass


class JobDetails(JobBase):
    id: int
    created_at: datetime


class JobUpdate(JobBaseModel):
    role: str | None = None
    company: str | None = None
    location: str | None = None
    work_arrangement: Arrangement | None
    status: Status | None = None
    source_link: str | None = None
    interview_date: date | None = None
    interview_time: time | None = None

    @field_validator("source_link", "interview_date", "interview_time", mode="before")
    @classmethod
    def ensure_none(cls, value: str | None):
        if isinstance(value, str) and len(value) == 0:
            return None
        return value

    @field_validator("interview_time", mode="before")
    @classmethod
    def ensure_time(cls, value: str):
        if isinstance(value, str) and len(value) > 0:
            return datetime.strptime(value, "%I:%M %p").time()
        return value
