from typing import Dict, Any

from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from recruiter.forms import CompanyForm, RecruiterSignupForm
from job_board.users.constants import Role
from common.mixins import RolePermissionMixin
from .models import Company


class RecruiterSignupView(views.SignupView):
    form_class = RecruiterSignupForm
    template_name = "account/recruiter_signup.html"

    def get_form_class(self):
        return self.form_class

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["role"] = Role.RECRUITER.name
        return kwargs


class RecruiterDashboardView(RolePermissionMixin, TemplateView, LoginRequiredMixin):
    template_name = "recruiter/dashboard.html"
    role = Role.RECRUITER

class CompanyCreateView(RolePermissionMixin, CreateView):
    role = Role.RECRUITER
    form_class = CompanyForm
    success_url = reverse_lazy("recruiter:dashboard")
    model = Company
