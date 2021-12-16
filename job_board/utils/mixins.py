from typing import Any

from django import http
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseBase, HttpResponseForbidden


class RolePermissionMixin:
    role = None

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        if self.role is None or request.user.role != self.role:
            raise PermissionDenied
        return super(RolePermissionMixin, self).dispatch(request, *args, **kwargs)
