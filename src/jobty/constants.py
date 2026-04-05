from enum import Enum


class Colors(Enum):
    red = "#ef4444"
    emerald = "#34d399"
    amber = "#fbbf24"
    gray = "#9ca3af"


class Status(Enum):
    applied = "Applied"
    interview = "Interview"
    hired = "Hired"
    rejected = "Rejected"


class Arrangement(Enum):
    onsite = "Onsite"
    hybrid = "Hybrid"
    remote = "Remote"
