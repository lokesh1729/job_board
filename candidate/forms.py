from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.utils.translation import gettext_lazy as _
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget

from candidate.models import (
    CandidateEducation,
    CandidateExperience,
    CandidateMisc,
    CandidatePreference,
    CandidateProject,
    CandidateSkill,
)
from job_board.users.forms import BaseSignupForm


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


class CandidateExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.candidate = kwargs.pop("candidate", None)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.disable_csrf = True
        self.helper.add_layout(
            layout=Layout(
                Row(Column("company"), Column("role")),
                "responsibilities",
                Row(Column("from_date"), Column("to_date")),
                "id",
            )
        )
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.candidate = self.candidate
        return super(CandidateExperienceForm, self).save(commit=commit)

    class Meta:
        model = CandidateExperience
        fields = ("id", "from_date", "to_date", "company", "role", "responsibilities")
        widgets = {
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
        }


class CandidateProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.candidate = kwargs.pop("candidate", None)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.disable_csrf = True
        self.helper.add_layout(
            layout=Layout("name", "description", "skills_used", "id")
        )
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.candidate = self.candidate
        return super(CandidateProjectForm, self).save(commit=commit)

    class Meta:
        model = CandidateProject
        fields = ("id", "name", "description", "skills_used")
        widgets = {
            "skills_used": ModelSelect2MultipleWidget(search_fields=["name__icontains"])
        }


class CandidateSkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.candidate = kwargs.pop("candidate", None)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.disable_csrf = True
        self.helper.add_layout(
            layout=Layout("skill", Row(Column("proficiency"), Column("yoe")), "id")
        )
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.candidate.onboarding_done = True
        self.candidate.save()
        self.instance.candidate = self.candidate
        return super(CandidateSkillForm, self).save(commit=commit)

    class Meta:
        model = CandidateSkill
        fields = ("id", "skill", "proficiency", "yoe")
        widgets = {
            "skill": ModelSelect2Widget(search_fields=["name__icontains"]),
        }


class CandidatePreferenceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.candidate = kwargs.pop("candidate", None)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.disable_csrf = True
        self.helper.add_layout(
            layout=Layout(
                "id",
                "total_yoe",
                "current_city",
                "desired_cities",
                Row(
                    Column("current_salary"),
                    Column("expected_salary"),
                ),
                "job_search_status",
                "profile_privacy",
            ),
        )
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.candidate = self.candidate
        return super(CandidatePreferenceForm, self).save(commit=commit)

    class Meta:
        model = CandidatePreference
        fields = (
            "id",
            "current_city",
            "desired_cities",
            "current_salary",
            "expected_salary",
            "job_search_status",
            "profile_privacy",
            "total_yoe",
        )
        widgets = {
            "current_city": ModelSelect2Widget(search_fields=["name__icontains"]),
            "desired_cities": ModelSelect2MultipleWidget(
                search_fields=["name__icontains"]
            ),
        }
