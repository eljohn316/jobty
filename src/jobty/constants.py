from enum import Enum
from typing import Literal


class Colors(Enum):
    red = "#ef4444"
    emerald = "#34d399"
    amber = "#fbbf24"
    gray = "#9ca3af"


Arrangement = Literal["Onsite", "Hybrid", "Remote"]

Status = Literal["Applied", "Interview", "Hired", "Rejected"]
