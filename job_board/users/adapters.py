from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import resolve_url

from candidate.models import Candidate
from recruiter.models import Recruiter

from . import constants, utils

from job_board.users.models import UserProfile
from .constants import Role


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        profile = UserProfile.objects.create(
            role=form.role, user=user
        )
        user.profile = profile
        user.save()
        if form.role == constants.Role.RECRUITER.name:
            Recruiter.objects.create(profile=profile)
        elif form.role == constants.Role.CANDIDATE.name:
            Candidate.objects.create(resume=form.cleaned_data["resume"],
                                     profile=profile)

    def get_login_redirect_url(self, request):
        utils.set_user_role(request)
        if request.user.role == Role.CANDIDATE:
            if not request.user.profile.candidate.onboarding_done:
                return resolve_url("candidate:onboarding")
            return resolve_url("candidate:dashboard")
        if request.user.role == Role.RECRUITER:
            return resolve_url("recruiter:dashboard")
        if request.user.role == Role.ADMIN:
            return resolve_url("admin:index")

    def get_signup_redirect_url(self, request):
        return resolve_url("account:login")


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
