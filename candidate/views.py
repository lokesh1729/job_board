from typing import Dict, Any

from allauth.account import views

from job_board.users.constants import Role
from job_board.users.forms import BaseSignupForm


class CandidateSignupView(views.SignupView):

    form_class = BaseSignupForm

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["role"] = Role.CANDIDATE.name
        return kwargs

