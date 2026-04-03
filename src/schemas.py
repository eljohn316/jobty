from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_serializer
from constants import Arrangement, Status


class Job(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        str_min_length=1,
        validate_default=True,
        validate_assignment=True,
        use_enum_values=True,
    )

    role: str
    company_name: str
    location: str
    work_arrangement: Arrangement
    status: Status = Field(default=Status.applied)
    job_posting_url: HttpUrl

    @field_serializer("job_posting_url", when_used="unless-none")
    def serialize_job_posting_url(self, value: HttpUrl):
        return str(value)
