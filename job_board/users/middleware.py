from django.utils.deprecation import MiddlewareMixin

from . import utils


class RoleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        utils.set_user_role(request)
