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
    ACTIVELY_LOOKING = "actively_looking"
    PASSIVELY_LOOKING = "passively_looking"
    NOT_LOOKING = "not_looking"


class ProfilePrivacyChoices(Enum):
    NONE = "none"
    ALL = "all"
    ONLY_TO_WHOSE_JOBS_I_APPLIED_TO = "only_to_whose_jobs_i_applied_to"


class OnboardingSteps:
    EDUCATION = "education"
    WORK = "work"
    PROJECTS = "projects"
    SKILLS = "skills"

    ADD_REMOVE_BTN_MAPPING = [
        {
            "addBtnClass": "add-education",
            "dataAttrName": "data-edu-id",
            "removeBtnClass": "remove-education",
        },
        {
            "addBtnClass": "add-work",
            "dataAttrName": "data-work-id",
            "removeBtnClass": "remove-work",
        },
        {
            "addBtnClass": "add-project",
            "dataAttrName": "data-project-id",
            "removeBtnClass": "remove-project",
        },
        {
            "addBtnClass": "add-skill",
            "dataAttrName": "data-skill-id",
            "removeBtnClass": "remove-skill",
        },
    ]

    STEP_HEADER_MAPPING = [
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

    STEPS_MAPPING = [
        {
            "context_data": [],
            "name": EDUCATION,
            "action": "/candidate/onboarding/education",
            "data_group": EDUCATION,
            "data_link_to": EDUCATION,
            "add_btn_text": "Add Education",
            "add_btn_class": "add-education",
            "remove_btn_text": "Remove Education",
            "remove_btn_class": "remove-education",
            "rows": [
                [
                    {
                        "input_type": "text",
                        "label_text": "School",
                        "input_name": "edu-school",
                        "placeholder": "Enter the school name",
                        "value_attribute": "school_name",
                        "required": True,
                        "extra_classes": "tw-flex-shrink tw-flex-grow-2",
                    },
                    {
                        "input_type": "text",
                        "label_text": "Degree",
                        "input_name": "edu-degree",
                        "placeholder": "Enter the degree",
                        "value_attribute": "degree",
                        "required": True,
                        "extra_classes": "tw-flex-shrink-2 tw-flex-grow tw-ml-16",
                    },
                ],
                [
                    {
                        "input_type": "date",
                        "label_text": "From Date",
                        "input_name": "edu-from-date",
                        "placeholder": "Enter from date",
                        "value_attribute": "from_date",
                        "required": True,
                        "extra_classes": "tw-flex-shrink tw-flex-grow",
                    },
                    {
                        "input_type": "date",
                        "label_text": "To Date",
                        "input_name": "edu-to-date",
                        "placeholder": "Enter to date",
                        "value_attribute": "to_date",
                        "required": True,
                        "extra_classes": "tw-flex-shrink tw-flex-grow tw-ml-16",
                    },
                ],
            ],
        },
        {
            "context_data": [],
            "name": WORK,
            "action": "/candidate/onboarding/work",
            "data_group": WORK,
            "data_link_to": WORK,
            "add_btn_text": "Add Work",
            "add_btn_class": "add-work",
            "remove_btn_text": "Remove Work",
            "remove_btn_class": "remove-work",
            "rows": [
                [
                    {
                        "input_type": "text",
                        "label_text": "Company",
                        "input_name": "work-company",
                        "placeholder": "Enter the organization name",
                        "value_attribute": "company",
                        "required": True,
                        "extra_classes": "tw-flex-grow tw-flex-shrink",
                    },
                    {
                        "input_type": "text",
                        "label_text": "Role",
                        "input_name": "work-role",
                        "placeholder": "Enter the name of the role",
                        "value_attribute": "role",
                        "required": True,
                        "extra_classes": "tw-flex-grow tw-flex-shrink tw-ml-16",
                    },
                ],
                [
                    {
                        "input_type": "date",
                        "label_text": "From Date",
                        "input_name": "work-from-date",
                        "placeholder": "Enter from date",
                        "value_attribute": "from_date",
                        "required": True,
                        "extra_classes": "tw-flex-grow tw-flex-shrink",
                    },
                    {
                        "input_type": "date",
                        "label_text": "To Date",
                        "input_name": "work-to-date",
                        "placeholder": "Enter to date",
                        "value_attribute": "to_date",
                        "required": True,
                        "extra_classes": "tw-flex-grow tw-flex-shrink tw-ml-16",
                    },
                ],
                [
                    {
                        "input_type": "textarea",
                        "label_text": "Responsibilities",
                        "input_name": "work-responsibilities",
                        "placeholder": "Enter what you have done there!",
                        "value_attribute": "responsibilities",
                        "required": True,
                        "extra_classes": "tw-flex-grow tw-flex-shrink",
                        "rows": 5,
                    }
                ],
            ],
        },
        {
            "context_data": [],
            "name": PROJECTS,
            "action": "/candidate/onboarding/project",
            "data_group": PROJECTS,
            "data_link_to": PROJECTS,
            "add_btn_text": "Add Project",
            "add_btn_class": "add-project",
            "remove_btn_text": "Remove Project",
            "remove_btn_class": "remove-project",
            "rows": [
                [
                    {
                        "input_type": "text",
                        "label_text": "Project Name",
                        "input_name": "project-name",
                        "placeholder": "Enter the project name",
                        "value_attribute": "name",
                        "required": True,
                        "extra_classes": "tw-flex-grow tw-flex-shrink",
                    }
                ],
                [
                    {
                        "input_type": "textarea",
                        "label_text": "Project Description",
                        "input_name": "project-description",
                        "placeholder": "Enter the project description",
                        "value_attribute": "description",
                        "required": True,
                        "extra_classes": "tw-flex-grow tw-flex-shrink",
                    }
                ],
                [
                    {
                        "input_type": "text",
                        "label_text": "Skills Used",
                        "input_name": "project-skills",
                        "placeholder": "Enter the skills used",
                        "value_attribute": "skills",
                        "extra_elements": [
                            '<small class="form-text text-muted">\
                            Add comma separated skills. For example : python, django, html\
                         </small>'
                        ],
                        "extra_classes": "tw-flex-grow tw-flex-shrink",
                        "required": True,
                    }
                ],
            ],
        },
        {
            "context_data": [],
            "name": SKILLS,
            "action": "/candidate/onboarding/skill",
            "data-attr-name": SKILLS,
            "data_link_to": SKILLS,
            "add_btn_text": "Add Skill",
            "add_btn_class": "add-skill",
            "remove_btn_text": "Remove Skill",
            "remove_btn_class": "remove-skill",
            "rows": [
                [
                    {
                        "input_type": "text",
                        "label_text": "Skill Name",
                        "input_name": "skill-name",
                        "placeholder": "Enter the skill name",
                        "value_attribute": "name",
                        "extra_classes": "tw-flex-grow tw-flex-shrink tw-basis-1/2",
                        "required": True,
                    },
                    {
                        "input_type": "number",
                        "label_text": "Proficiency",
                        "input_name": "skill-proficiency",
                        "value_attribute": "proficiency",
                        "min": 1,
                        "max": 10,
                        "extra_elements": [
                            '<small class="form-text text-muted">'
                            "Note that minimum is 1, maximum is 10"
                            "</small>"
                        ],
                        "extra_classes": "tw-flex-grow tw-flex-shrink tw-basis-1/4",
                        "required": True,
                    },
                    {
                        "input_type": "number",
                        "label_text": "YOE",
                        "min": 0,
                        "max": 100,
                        "input_name": "skill-yoe",
                        "placeholder": "Enter the skills used",
                        "value_attribute": "yoe",
                        "extra_elements": [
                            '<small class="form-text text-muted">\
                            Add comma separated skills. For example : python, django, html\
                         </small>'
                        ],
                        "extra_classes": "tw-flex-grow tw-flex-shrink tw-basis-1/4",
                        "required": True,
                    },
                ]
            ],
        },
    ]
