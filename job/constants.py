from enum import Enum


class Remote(Enum):
    FULLY_REMOTE = "Fully Remote"
    NO_REMOTE = "No Remote"
    HYBRID = "Hybrid"

class JobType(Enum):
    FULL_TIME = "Full Time"
    PART_TIME = "Part Time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
