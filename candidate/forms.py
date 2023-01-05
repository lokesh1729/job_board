from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.utils.translation import gettext_lazy as _
from django_select2.forms import ModelSelect2Widget

from candidate.models import (
    CandidateEducation,
    CandidateExperience,
    CandidateMisc,
    CandidateProject,
    CandidateSkill,
)
from common.models import School
from job_board.users.forms import BaseSignupForm

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
        self.candidate = kwargs.pop("candidate", None)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.disable_csrf = True
        self.helper.add_layout(
            layout=Layout(
                "school", "degree", Row(Column("from_date"), Column("to_date")), "id"
            )
        )
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.candidate = self.candidate
        return super(CandidateEducationForm, self).save(commit=commit)

    class Meta:
        model = CandidateEducation
        fields = ("id", "school", "degree", "from_date", "to_date")
        widgets = {
            "school": ModelSelect2Widget(search_fields=["name__icontains"]),
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
        }
