from typing import Any
from typing import Dict

from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from candidate.forms import CandidateSignupForm
from candidate.models import Candidate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from job_board.users.constants import Role
from job_board.utils.mixins import RolePermissionMixin


class CandidateSignupView(views.SignupView):

    form_class = CandidateSignupForm
    template_name = "account/candidate_signup.html"

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["role"] = Role.CANDIDATE.name
        return kwargs


class CandidateDashboardView(LoginRequiredMixin, RolePermissionMixin, TemplateView):
    template_name = "candidate/dashboard.html"
    role = Role.CANDIDATE

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["candidate"] = self.request.user.profile.candidate
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.profile.candidate.onboarding_done:
            return redirect(reverse("candidate:onboarding"))


class CandidateOnboardingView(LoginRequiredMixin, RolePermissionMixin, TemplateView):
    template_name = "candidate/onboarding/main.html"
    role = Role.CANDIDATE

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["candidate"] = self.request.user.profile.candidate
        return super().get_context_data(**kwargs)


@user_passes_test(
    lambda user: user.profile
    and user.profile.candidate
    and isinstance(user.profile.candidate, Candidate)
)
@login_required
def education_details(request):
    if request.is_ajax() and request.method == "POST":
        data = request.POST.getlist("data[]")
        assert data is not None
        Candidate.objects.bulk_create([Candidate(**ele) for ele in data])
        return JsonResponse({"result": "success"})
