import copy
import json
import logging

from typing import Any
from typing import Dict

from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.db.models import F

from candidate.forms import CandidateSignupForm
from candidate.models import (
    CandidateEducation,
    CandidateSkill,
    CandidateProject,
    Candidate,
    School,
    CandidateExperience,
    Skill,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from job_board.users.constants import Role
from job_board.utils.mixins import RolePermissionMixin
from .constants import OnboardingSteps
from .utils import sanitize_data

logger = logging.getLogger(__name__)


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
        return super().get(request, *args, **kwargs)


class CandidateOnboardingView(LoginRequiredMixin, RolePermissionMixin, TemplateView):
    template_name = "candidate/onboarding/main.html"
    role = Role.CANDIDATE

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        candidate = self.request.user.profile.candidate
        projects = CandidateProject.objects.raw(
            """
            SELECT ARRAY_AGG("skills") as skills, id, name, description
                FROM (
                        SELECT "candidate_candidateproject"."id",
                            "candidate_candidateproject"."name",
                            "candidate_candidateproject"."description",
                            "candidate_skill"."name" AS "skills"
                            FROM "candidate_candidateproject"
                            LEFT OUTER JOIN "candidate_candidateproject_skills_used"
                            ON ("candidate_candidateproject"."id" = "candidate_candidateproject_skills_used"."candidateproject_id")
                            LEFT OUTER JOIN "candidate_skill"
                            ON ("candidate_candidateproject_skills_used"."skill_id" = "candidate_skill"."id")
                        WHERE "candidate_candidateproject"."candidate_id" = %s
                ) as tbl1 GROUP BY id, name, description;
            """
            % candidate.pk
        )
        form_data = copy.deepcopy(OnboardingSteps.STEPS_MAPPING)
        form_data[0]["context_data"] = candidate.candidate_educations.values(
            "pk", "degree", "from_date", "to_date", school_name=F("school__name")
        )
        form_data[1]["context_data"] = candidate.candidate_experiences.values(
            "pk", "company", "role", "responsibilities", "from_date", "to_date"
        )
        form_data[2]["context_data"] = list(
            map(
                lambda project: {
                    "pk": project.id,
                    "name": project.name,
                    "description": project.description,
                    "skills": ", ".join(project.skills),
                },
                projects,
            )
        )
        form_data[3]["context_data"] = candidate.candidate_skills.values(
            "pk",
            proficiency=F("skill__proficiency"),
            yoe=F("skill__yoe"),
            name=F("skill__name"),
        )
        return {
            **context,
            "candidate": candidate,
            "step_header_mapping": OnboardingSteps.STEP_HEADER_MAPPING,
            "form_data": form_data,
        }


@login_required
@user_passes_test(
    lambda user: user.profile
    and user.profile.candidate
    and isinstance(user.profile.candidate, Candidate)
)
def education_details(request):
    if request.is_ajax() and request.method == "POST":
        req_body = json.loads(request.body)
        candidate = request.user.profile.candidate
        logger.info("education_details : got req_body %s for candidate %s", req_body, candidate)
        data = req_body["data"]
        assert data is not None
        data = sanitize_data(data)
        result = []
        for ele in data:
            school, _ = School.objects.get_or_create(name=ele["edu-school"])
            if "pk" not in ele:
                result.append(
                    CandidateEducation.objects.create(
                        candidate=candidate,
                        school=school,
                        degree=ele["edu-degree"],
                        from_date=ele["edu-from-date"],
                        to_date=ele["edu-to-date"],
                    ).pk
                )
            else:
                CandidateEducation.objects.filter(pk=ele["pk"]).update(
                    school=school,
                    degree=ele["edu-degree"],
                    from_date=ele["edu-from-date"],
                    to_date=ele["edu-to-date"],
                )
                result.append(ele["pk"])
        logger.info("result is %s", result)
        return JsonResponse({"result": result})
    else:
        return HttpResponseBadRequest("bad request")


@login_required
@user_passes_test(
    lambda user: user.profile
    and user.profile.candidate
    and isinstance(user.profile.candidate, Candidate)
)
def work_details(request):
    if request.is_ajax() and request.method == "POST":
        req_body = json.loads(request.body)
        candidate = request.user.profile.candidate
        logger.info("work_details : got req_body %s for candidate %s", req_body, candidate)
        data = req_body["data"]
        assert data is not None
        data = sanitize_data(data)
        result = []
        for ele in data:
            if "pk" not in ele:
                result.append(
                    CandidateExperience.objects.create(
                        candidate=candidate,
                        from_date=ele["work-from-date"],
                        to_date=ele["work-to-date"],
                        company=ele["work-company"],
                        role=ele["work-role"],
                        responsibilities=ele["work-responsibilities"],
                    ).pk
                )
            else:
                CandidateExperience.objects.filter(pk=ele["pk"]).update(
                    from_date=ele["work-from-date"],
                    to_date=ele["work-to-date"],
                    company=ele["work-company"],
                    role=ele["work-role"],
                    responsibilities=ele["work-responsibilities"],
                )
                result.append(ele["pk"])
        logger.info("result is %s", result)
        return JsonResponse({"result": result})
    else:
        return HttpResponseBadRequest("bad request")


@login_required
@user_passes_test(
    lambda user: user.profile
    and user.profile.candidate
    and isinstance(user.profile.candidate, Candidate)
)
def project_details(request):
    if request.is_ajax() and request.method == "POST":
        req_body = json.loads(request.body)
        candidate = request.user.profile.candidate
        logger.info("project_details : got req_body %s for candidate %s", req_body, candidate)
        data = req_body["data"]
        assert data is not None
        data = sanitize_data(data)
        result = []
        for ele in data:
            skills = []
            for skill in ele["project-skills"].split(","):
                skill = skill.strip()
                s_obj, _ = Skill.objects.get_or_create(name=skill)
                skills.append(s_obj)
            if "pk" not in ele:
                obj = CandidateProject.objects.create(
                    candidate=candidate,
                    name=ele["project-name"],
                    description=ele["project-description"],
                )
                obj.skills_used.set(skills)
                result.append(obj.pk)
            else:
                obj = CandidateProject.objects.get(pk=ele["pk"])
                obj.name = ele["project-name"]
                obj.description = ele["project-description"]
                obj.skills_used.set(skills)
                obj.save()
                result.append(ele["pk"])
        logger.info("result is %s", result)
        return JsonResponse({"result": result})
    else:
        return HttpResponseBadRequest("bad request")


@login_required
@user_passes_test(
    lambda user: user.profile
    and user.profile.candidate
    and isinstance(user.profile.candidate, Candidate)
)
def skill_details(request):
    if request.is_ajax() and request.method == "POST":
        req_body = json.loads(request.body)
        candidate = request.user.profile.candidate
        logger.info("skill_details : got req_body %s for candidate %s", req_body, candidate)
        data = req_body["data"]
        assert data is not None
        data = sanitize_data(data)
        result = []
        for ele in data:
            skill, _ = Skill.objects.update_or_create(
                name=ele["skill-name"],
                defaults={
                    "proficiency": int(ele["skill-proficiency"]),
                    "yoe": int(ele["skill-yoe"]),
                },
            )
            if "pk" not in ele:
                result.append(
                    CandidateSkill.objects.create(candidate=candidate, skill=skill).pk
                )
            else:
                CandidateSkill.objects.filter(pk=ele["pk"]).update(skill=skill)
                result.append(ele["pk"])
        candidate.onboarding_done = True
        candidate.save()
        logger.info("result is %s", result)
        return JsonResponse({"result": result})
    else:
        return HttpResponseBadRequest("bad request")
