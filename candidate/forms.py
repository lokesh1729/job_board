from pathlib import Path
from job_board.users.forms import BaseSignupForm
from django import forms
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = Path("%s/resume.pdf" % settings.MEDIA_ROOT)
        self.fields["resume"].initial = File(path)
        self.fields["resume"].initial.url = default_storage.url("resume.pdf")
