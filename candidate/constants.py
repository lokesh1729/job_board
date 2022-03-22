"""
constants for candidate
"""
from enum import Enum


class Proficiency(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10


class OnboardingSteps:
    EDUCATION = "education"
    WORK = "work"
    PROJECTS = "projects"
    SKILLS = "skills"

    STEP_HEADER_MAPPING = [
        {
            "name": EDUCATION,
            "icon": "fas fa-school step-icon",
            "data_link_to": "education-details",
        },
        {
            "name": WORK,
            "icon": "fas fa-briefcase step-icon",
            "data_link_to": "work-details",
        },
        {
            "name": PROJECTS,
            "icon": "fas fa-project-diagram step-icon",
            "data_link_to": "project-details",
        },
        {
            "name": SKILLS,
            "icon": "fas fa-tasks step-icon",
            "data_link_to": "skill-details",
        },
    ]
