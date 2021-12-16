from job_board.users.forms import BaseSignupForm
from django import forms
from django.utils.translation import gettext_lazy as _


class EmployerSignupForm(BaseSignupForm):
    employer_name = forms.CharField(required=True, label=_("Employer Name"), widget=forms.TextInput(
            attrs={"placeholder": _("Employer Name"), "autocomplete": "employer_name"}
        ),)
    employer_industry = forms.CharField(required=True, label=_("Employer Industry"), widget=forms.TextInput(
            attrs={"placeholder": _("Employer Industry"), "autocomplete": "employer_industry"}
        ))
