from django.contrib.auth.models import AnonymousUser

from job_board.users.constants import Role


def set_user_role(request):
    request.user.role = AnonymousUser()
    if request.user.is_authenticated:
        request.user.role = Role[request.user.profile.role]
