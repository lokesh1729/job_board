from typing import Dict, Any

from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from recruiter.forms import CompanyForm, RecruiterSignupForm
from job_board.users.constants import Role
from common.mixins import RolePermissionMixin
from .models import Company
from job.models import Job
from . import repositories


class RecruiterSignupView(views.SignupView):
    form_class = RecruiterSignupForm
    template_name = "account/recruiter_signup.html"

    def get_form_class(self):
        return self.form_class

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["role"] = Role.RECRUITER.name
        return kwargs


class RecruiterDashboardView(LoginRequiredMixin, RolePermissionMixin, TemplateView):
    template_name = "recruiter/dashboard.html"
    role = Role.RECRUITER

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "jobs": repositories.list_jobs(self.request.user.profile.recruiter),
                "display_edit_row": True,
            }
        )
        return context


class CompanyCreateView(LoginRequiredMixin, RolePermissionMixin, CreateView):
    role = Role.RECRUITER
    form_class = CompanyForm
    success_url = reverse_lazy("recruiter:dashboard")
    model = Company
