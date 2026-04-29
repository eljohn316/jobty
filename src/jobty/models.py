from datetime import UTC, date, datetime, time
from typing import Literal

from sqlalchemy import Date, DateTime, Integer, String, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    role: Mapped[str] = mapped_column(String, nullable=False)
    company: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    work_arrangement: Mapped[Literal["Onsite", "Hybrid", "Remote"]] = mapped_column(
        String, nullable=False
    )
    status: Mapped[Literal["Applied", "Interview", "Hired", "Rejected"]] = (
        mapped_column(String, nullable=False)
    )
    source_link: Mapped[str | None] = mapped_column(String, nullable=True)
    interview_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    interview_time: Mapped[time | None] = mapped_column(Time, nullable=True)

    __table_args__ = (UniqueConstraint("role", "company", name="unq_role_company"),)
