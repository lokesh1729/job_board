import json

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
from .constants import OnboardingSteps


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
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "candidate": self.request.user.profile.candidate,
            "step_header_mapping": OnboardingSteps.STEP_HEADER_MAPPING,
        }


@user_passes_test(
    lambda user: user.profile
    and user.profile.candidate
    and isinstance(user.profile.candidate, Candidate)
)
@login_required
def education_details(request):
    if request.is_ajax() and request.method == "POST":
        req_body = json.loads(request.body)
        data = req_body["data"]
        form_type = req_body["form_type"]
        candidate = request.user.profile.candidate
        assert form_type is not None
        assert data is not None
        result = []
        if form_type == OnboardingSteps.EDUCATION:
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
            for _obj in CandidateEducation.objects.bulk_create(objs):
                result.append(_obj.pk)
        elif form_type == OnboardingSteps.WORK:
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
            for _obj in CandidateExperience.objects.bulk_create(objs):
                result.append(_obj.pk)
        elif form_type == OnboardingSteps.PROJECTS:
            for ele in data:
                if "pk" not in ele:
                    obj = CandidateProject.objects.create(
                        candidate=candidate,
                        name=ele["project-name"],
                        description=ele["project-description"],
                    )
                    skills = []
                    for skill in ele["skills"].split(","):
                        s_obj, _ = Skill.objects.get_or_create(name=skill["skill_name"])
                        skills.append(s_obj)
                    obj.skills_used.set(skills)
                    result.append(obj.pk)
        elif form_type == OnboardingSteps.SKILLS:
            objs = []
            for ele in data:
                if "pk" not in ele:
                    skill, _ = Skill.objects.get_or_create(name=ele["skill_name"])
                    objs.append(
                        CandidateSkill(
                            candidate=candidate,
                            skill=skill,
                            proficiency=int(ele["skill_proficiency"]),
                            yoe=int(ele["skill_yoe"]),
                        )
                    )
            for _obj in CandidateSkill.objects.bulk_create(objs):
                result.append(_obj.pk)
        return JsonResponse({"result": result})
