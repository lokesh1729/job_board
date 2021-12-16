from job_board.users.forms import BaseSignupForm
from django import forms
from django.utils.translation import gettext_lazy as _


class CandidateSignupForm(BaseSignupForm):
    resume = forms.FileField(required=False, label=_("Upload your resume (optional)"), widget=forms.FileInput(
            attrs={"placeholder": _("Resume")}
        ))
