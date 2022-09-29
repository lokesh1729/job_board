from typing import Any

from django import http
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBase, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

from job_board.users.constants import Role


class RolePermissionMixin:
    role = None

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        if self.role is None or request.user.role != self.role:
            raise PermissionDenied
        return super(RolePermissionMixin, self).dispatch(request, *args, **kwargs)


class LoginRedirectMixin:

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        import ipdb;ipdb.set_trace()
        if request.user.is_authenticated:
            if request.user is not None and hasattr(request.user, "role"):
                if request.user.role == Role.Candidate:
                    return redirect(reverse("candidate:onboarding"))
                if request.user.role == Role.EMPLOYER:
                    return redirect(reverse("employer:dashboard"))
        return super(LoginRedirectMixin, self).dispatch(request, *args, **kwargs)
