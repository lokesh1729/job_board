from typing import Dict, Any

from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from employer.forms import EmployerSignupForm
from employer.models import Employer
from job_board.users.constants import Role
from job_board.utils.mixins import RolePermissionMixin


class EmployerSignupView(views.SignupView):
    form_class = EmployerSignupForm
    template_name = "account/employer_signup.html"

    def get_form_class(self):
        return self.form_class

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["role"] = Role.EMPLOYER.name
        return kwargs


class EmployerDashboardView(RolePermissionMixin, TemplateView, LoginRequiredMixin):
    template_name = "emp_dashboard.html"
    role = Role.EMPLOYER
