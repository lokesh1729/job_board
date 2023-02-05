import logging
from typing import Any, Dict

from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from candidate.forms import (
    CandidateEducationForm,
    CandidateExperienceForm,
    CandidatePreferenceForm,
    CandidateProjectForm,
    CandidateSignupForm,
    CandidateSkillForm,
)
from candidate.models import (
    CandidateEducation,
    CandidateExperience,
    CandidatePreference,
    CandidateProject,
    CandidateSkill,
)
from common.mixins import RolePermissionMixin
from job_board.users.constants import Role

from .constants import OnboardingSteps

logger = logging.getLogger(__name__)


class CandidateSignupView(views.SignupView):

    form_class = CandidateSignupForm
    template_name = "account/candidate_signup.html"

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["role"] = Role.CANDIDATE
        return kwargs


class CandidateDashboardView(LoginRequiredMixin, RolePermissionMixin, TemplateView):
    template_name = "candidate/dashboard.html"
    role = Role.CANDIDATE

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["candidate"] = self.request.user.profile.candidate
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.profile.candidate.onboarding_done:
            return redirect(reverse("candidate:preferences"))
        return super().get(request, *args, **kwargs)


class CandidatePreferenceView(LoginRequiredMixin, RolePermissionMixin, FormView):
    template_name = "candidate/onboarding/main.html"
    role = Role.CANDIDATE
    success_url = reverse_lazy("candidate:education")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        return super().form_valid(form)

    def get_form_class(self):
        extra = 1
        if len(self.get_initial()) > 0:
            extra = 0
        return modelformset_factory(
            CandidatePreference, form=CandidatePreferenceForm, extra=extra
        )

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["form_kwargs"] = {"candidate": self.request.user.profile.candidate}
        return kwargs

    def get_initial(self) -> Dict[str, Any]:
        return CandidatePreference.objects.filter(
            candidate=self.request.user.profile.candidate
        ).values(
            "id",
            "current_city",
            "desired_cities",
            "expected_salary",
            "current_salary",
            "job_search_status",
            "profile_privacy",
            "total_yoe",
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "step_header_mapping": OnboardingSteps.STEP_HEADER_MAPPING,
                "step_header_sequence": list(
                    map(
                        lambda x: x["data_link_to"], OnboardingSteps.STEP_HEADER_MAPPING
                    )
                ),
                "form_action": reverse("candidate:preferences"),
                "form_id": OnboardingSteps.CANDIDATE_PREFERENCES,
                "btn_mapping": OnboardingSteps.ADD_REMOVE_BTN_MAPPING,
                "show_add_remove_btn": False,
                "success_url": self.get_success_url(),
            }
        )
        return context


class CandidateEducationNew(LoginRequiredMixin, RolePermissionMixin, FormView):
    template_name = "candidate/onboarding/main.html"
    role = Role.CANDIDATE
    success_url = reverse_lazy("candidate:work")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        return super().form_valid(form)

    def get_form_class(self):
        extra = 1
        if len(self.get_initial()) > 0:
            extra = 0
        return modelformset_factory(
            CandidateEducation, form=CandidateEducationForm, extra=extra
        )

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["form_kwargs"] = {"candidate": self.request.user.profile.candidate}
        return kwargs

    def get_initial(self) -> Dict[str, Any]:
        return CandidateEducation.objects.filter(
            candidate=self.request.user.profile.candidate
        ).values("id", "school", "degree", "from_date", "to_date")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "step_header_mapping": OnboardingSteps.STEP_HEADER_MAPPING,
                "step_header_sequence": list(
                    map(
                        lambda x: x["data_link_to"], OnboardingSteps.STEP_HEADER_MAPPING
                    )
                ),
                "form_action": reverse("candidate:education"),
                "form_id": OnboardingSteps.EDUCATION,
                "show_add_remove_btn": True,
                "add_btn_class": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.EDUCATION
                ]["add_btn_class"],
                "add_btn_text": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.EDUCATION
                ]["add_btn_text"],
                "remove_btn_text": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.EDUCATION
                ]["remove_btn_text"],
                "remove_btn_class": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.EDUCATION
                ]["remove_btn_class"],
                "btn_mapping": OnboardingSteps.ADD_REMOVE_BTN_MAPPING,
                "success_url": self.get_success_url(),
            }
        )
        return context


class CandidateWorkView(LoginRequiredMixin, RolePermissionMixin, FormView):
    template_name = "candidate/onboarding/main.html"
    role = Role.CANDIDATE
    success_url = reverse_lazy("candidate:projects")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        return super().form_valid(form)

    def get_form_class(self):
        extra = 1
        if len(self.get_initial()) > 0:
            extra = 0
        return modelformset_factory(
            CandidateExperience, form=CandidateExperienceForm, extra=extra
        )

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["form_kwargs"] = {"candidate": self.request.user.profile.candidate}
        return kwargs

    def get_initial(self) -> Dict[str, Any]:
        return CandidateExperience.objects.filter(
            candidate=self.request.user.profile.candidate
        ).values("id", "company", "role", "responsibilities", "from_date", "to_date")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "step_header_mapping": OnboardingSteps.STEP_HEADER_MAPPING,
                "step_header_sequence": list(
                    map(
                        lambda x: x["data_link_to"], OnboardingSteps.STEP_HEADER_MAPPING
                    )
                ),
                "form_action": reverse("candidate:work"),
                "form_id": OnboardingSteps.WORK,
                "show_add_remove_btn": True,
                "add_btn_class": OnboardingSteps.STEPS_MAPPING[OnboardingSteps.WORK][
                    "add_btn_class"
                ],
                "add_btn_text": OnboardingSteps.STEPS_MAPPING[OnboardingSteps.WORK][
                    "add_btn_text"
                ],
                "remove_btn_text": OnboardingSteps.STEPS_MAPPING[OnboardingSteps.WORK][
                    "remove_btn_text"
                ],
                "remove_btn_class": OnboardingSteps.STEPS_MAPPING[OnboardingSteps.WORK][
                    "remove_btn_class"
                ],
                "btn_mapping": OnboardingSteps.ADD_REMOVE_BTN_MAPPING,
                "success_url": self.get_success_url(),
            }
        )
        return context


class CandidateProjectView(LoginRequiredMixin, RolePermissionMixin, FormView):
    template_name = "candidate/onboarding/main.html"
    role = Role.CANDIDATE
    success_url = reverse_lazy("candidate:skills")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        return super().form_valid(form)

    def get_form_class(self):
        extra = 1
        if len(self.get_initial()) > 0:
            extra = 0
        return modelformset_factory(
            CandidateProject, form=CandidateProjectForm, extra=extra
        )

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["form_kwargs"] = {"candidate": self.request.user.profile.candidate}
        return kwargs

    def get_initial(self) -> Dict[str, Any]:
        return CandidateProject.objects.filter(
            candidate=self.request.user.profile.candidate
        ).values("id", "name", "description", "skills_used")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "step_header_mapping": OnboardingSteps.STEP_HEADER_MAPPING,
                "step_header_sequence": list(
                    map(
                        lambda x: x["data_link_to"], OnboardingSteps.STEP_HEADER_MAPPING
                    )
                ),
                "form_action": reverse("candidate:projects"),
                "show_add_remove_btn": True,
                "form_id": OnboardingSteps.PROJECTS,
                "add_btn_class": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.PROJECTS
                ]["add_btn_class"],
                "add_btn_text": OnboardingSteps.STEPS_MAPPING[OnboardingSteps.PROJECTS][
                    "add_btn_text"
                ],
                "remove_btn_text": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.PROJECTS
                ]["remove_btn_text"],
                "remove_btn_class": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.PROJECTS
                ]["remove_btn_class"],
                "btn_mapping": OnboardingSteps.ADD_REMOVE_BTN_MAPPING,
                "success_url": self.get_success_url(),
            }
        )
        return context


class CandidateSkillView(LoginRequiredMixin, RolePermissionMixin, FormView):
    template_name = "candidate/onboarding/main.html"
    role = Role.CANDIDATE
    success_url = reverse_lazy("candidate:dashboard")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.save()
        return super().form_valid(form)

    def get_form_class(self):
        extra = 1
        if len(self.get_initial()) > 0:
            extra = 0
        return modelformset_factory(
            CandidateSkill, form=CandidateSkillForm, extra=extra
        )

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["form_kwargs"] = {"candidate": self.request.user.profile.candidate}
        return kwargs

    def get_initial(self) -> Dict[str, Any]:
        return CandidateSkill.objects.filter(
            candidate=self.request.user.profile.candidate
        ).values("id", "skill", "proficiency", "yoe")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "step_header_mapping": OnboardingSteps.STEP_HEADER_MAPPING,
                "step_header_sequence": list(
                    map(
                        lambda x: x["data_link_to"], OnboardingSteps.STEP_HEADER_MAPPING
                    )
                ),
                "form_action": reverse("candidate:skills"),
                "form_id": OnboardingSteps.SKILLS,
                "show_add_remove_btn": True,
                "add_btn_class": OnboardingSteps.STEPS_MAPPING[OnboardingSteps.SKILLS][
                    "add_btn_class"
                ],
                "add_btn_text": OnboardingSteps.STEPS_MAPPING[OnboardingSteps.SKILLS][
                    "add_btn_text"
                ],
                "remove_btn_text": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.SKILLS
                ]["remove_btn_text"],
                "remove_btn_class": OnboardingSteps.STEPS_MAPPING[
                    OnboardingSteps.SKILLS
                ]["remove_btn_class"],
                "btn_mapping": OnboardingSteps.ADD_REMOVE_BTN_MAPPING,
                "success_url": self.get_success_url(),
            }
        )
        return context
