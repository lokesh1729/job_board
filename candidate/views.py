from typing import Any
from typing import Dict

from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from candidate.forms import CandidateSignupForm
from candidate.models import (
    Candidate,
    CandidateEducation,
    CandidateSkill,
    Candidate,
    School,
    CandidateExperience,
)
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
        form_type = request.POST.get("form_type")
        candidate = request.user.profile.candidate
        assert form_type is not None
        assert data is not None
        if form_type == "education":
            objs = []
            for ele in data:
                if "pk" not in ele:
                    school, _ = School.objects.get_or_create(name=ele["school"])
                    objs.append(
                        CandidateEducation(
                            candidate=candidate,
                            school=school,
                            degree=ele["degree"],
                            from_date=ele["from-date"],
                            to_date=ele["to-date"],
                        )
                    )
            CandidateEducation.objects.bulk_create(objs)
        elif form_type == "work":
            objs = []
            for ele in data:
                if "pk" not in ele:
                    objs.append(
                        CandidateExperience(
                            candidate=candidate,
                            from_date=ele["from-date"],
                            to_date=ele["to-date"],
                            company=ele["company"],
                            role=ele["role"],
                            responsibilities=ele["responsibilities"],
                        )
                    )
            CandidateExperience.objects.bulk_create(objs)
        elif form_type == "projects":
            objs = []
            for ele in data:
                if "pk" not in ele:
                    obj = CandidateProject.objects.create(
                        candidate=candidate,
                        name=ele["project-name"],
                        description=ele["project-description"],
                    )
                    skills = []
                    for skill in ele["skills"].split(","):
                        s_obj = Skill.objects.get_or_create(name=skill["skill_name"])
                        skills.append(s_obj)
                    obj.skills_used.set(skills)
        elif form_type == "skills":
            objs = []
            for ele in data:
                if "pk" not in ele:
                    skill = Skill.objects.get_or_create(name=ele["skill_name"])
                    objs.append(
                        CandidateSkill(
                            candidate=candidate,
                            skill=skill,
                            proficiency=int(ele["skill_proficiency"]),
                            yoe=int(ele["skill_yoe"]),
                        )
                    )
            CandidateSkill.objects.bulk_create(objs)
        return JsonResponse({"result": "success"})
