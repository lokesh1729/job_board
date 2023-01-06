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


class JobSearchChoices(Enum):
    ACTIVELY_LOOKING = "Actively Looking"
    PASSIVELY_LOOKING = "Passively Looking"
    NOT_LOOKING = "Not Looking At The Moment"


class ProfilePrivacyChoices(Enum):
    NONE = "No one! Hide from everyone"
    ALL = "Everyone!"
    ONLY_TO_WHOSE_JOBS_I_APPLIED_TO = "Recruiters to whose jobs I applied!"


class OnboardingSteps:
    EDUCATION = "education"
    WORK = "work"
    PROJECTS = "projects"
    SKILLS = "skills"
    CANDIDATE_PREFERENCES = "preferences"

    ADD_REMOVE_BTN_MAPPING = [
        {
            "addBtnClass": "add-education",
            "removeBtnClass": "remove-education",
        },
        {
            "addBtnClass": "add-work",
            "removeBtnClass": "remove-work",
        },
        {
            "addBtnClass": "add-project",
            "removeBtnClass": "remove-project",
        },
        {
            "addBtnClass": "add-skill",
            "removeBtnClass": "remove-skill",
        },
    ]

    STEP_HEADER_MAPPING = [
        {
            "name": "Basic Info",
            "data_link_to": CANDIDATE_PREFERENCES,
            "icon": "fas fa-user step-icon",
        },
        {
            "name": "Education",
            "data_link_to": EDUCATION,
            "icon": "fas fa-school step-icon",
        },
        {"name": "Work", "data_link_to": WORK, "icon": "fas fa-briefcase step-icon"},
        {
            "name": "Projects",
            "data_link_to": PROJECTS,
            "icon": "fas fa-project-diagram step-icon",
        },
        {"name": "Skills", "data_link_to": SKILLS, "icon": "fas fa-tasks step-icon"},
    ]

    STEPS_MAPPING = {
        EDUCATION: {
            "add_btn_text": "Add Education",
            "add_btn_class": "add-education",
            "remove_btn_text": "Remove Education",
            "remove_btn_class": "remove-education",
        },
        WORK: {
            "add_btn_text": "Add Work",
            "add_btn_class": "add-work",
            "remove_btn_text": "Remove Work",
            "remove_btn_class": "remove-work",
        },
        PROJECTS: {
            "add_btn_text": "Add Project",
            "add_btn_class": "add-project",
            "remove_btn_text": "Remove Project",
            "remove_btn_class": "remove-project",
        },
        SKILLS: {
            "add_btn_text": "Add Skill",
            "add_btn_class": "add-skill",
            "remove_btn_text": "Remove Skill",
            "remove_btn_class": "remove-skill",
        },
    }
