from job_board.users.forms import BaseSignupForm
from django import forms
from django.utils.translation import gettext_lazy as _

from recruiter.models import Company


class RecruiterSignupForm(BaseSignupForm):
    pass


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("name", "logo", "url", "industry", "location", "size", "about")
