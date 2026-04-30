from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, field_serializer

from .constants import Arrangement, Status


class JobBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
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
    status: Status
    source_link: str | None = None
    interview_date: date | None = None
    interview_time: time | None = None

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

    @field_serializer("created_at", mode="plain")
    def ser_created_at(self, value: datetime):
        return value.strftime("%b %-d, %Y - %I:%M %p")


class JobUpdate(JobBaseModel):
    role: str | None = None
    company: str | None = None
    location: str | None = None
    work_arrangement: Arrangement | None
    status: Status | None = None
    source_link: str | None = None
    interview_date: date | None = None
    interview_time: time | None = None
