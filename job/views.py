from typing import Any, Dict
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from common.mixins import RolePermissionMixin

from .models import Job
from .forms import JobForm
from job_board.users.constants import Role


class JobView(LoginRequiredMixin, RolePermissionMixin, CreateView):
    role = Role.RECRUITER
    model = Job
    form_class = JobForm
    success_url = reverse_lazy("recruiter:dashboard")

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({"posted_by": self.request.user.profile.recruiter})
        return kwargs
