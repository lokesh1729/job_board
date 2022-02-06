from job_board.users.forms import BaseSignupForm
from django import forms
from django.utils.translation import gettext_lazy as _


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
