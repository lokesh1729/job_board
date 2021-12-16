from typing import Dict, Any

from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from candidate.forms import CandidateSignupForm
from candidate.models import Candidate
from job_board.users.constants import Role
from job_board.utils.mixins import RolePermissionMixin


class CandidateSignupView(views.SignupView):

    form_class = CandidateSignupForm
    template_name = "account/candidate_signup.html"

    def get_form_class(self):
        return self.form_class

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["role"] = Role.CANDIDATE.name
        return kwargs


class CandidateDashboardView(RolePermissionMixin, LoginRequiredMixin, TemplateView):
    template_name = "cand_dashboard.html"
    role = Role.CANDIDATE.value
