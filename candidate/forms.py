from job_board.users.forms import BaseSignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from candidate.models import (
    CandidateEducation,
    CandidateExperience,
    CandidateProject,
    CandidateSkill,
    CandidateMisc,
)
from common.models import School
from django_select2.forms import ModelSelect2Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from . import constants


class CandidateSignupForm(BaseSignupForm):

    resume = forms.FileField(
        required=True,
        label=_("Upload your resume"),
        widget=forms.ClearableFileInput(
            attrs={
                "required": True,
                "id": "id_resume",
                "accept": ".pdf,.doc,.docx,application/msword,"
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            }
        ),
    )


class CandidateEducationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "candidate:education"
        self.helper.form_id = constants.OnboardingSteps.EDUCATION
        self.helper.form_class = "form--wrapper needs-validation"
        self.helper.add_layout(
            layout=Layout(
                "school",
                "degree",
                Row(Column("from_date"), Column("to_date")),
            )
        )

    class Meta:
        model = CandidateEducation
        fields = ("school", "degree", "from_date", "to_date")
        widgets = {
            "school": ModelSelect2Widget(search_fields=["name__icontains"]),
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
        }
