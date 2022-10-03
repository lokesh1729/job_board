from django import template

from job_board.users.constants import Role

register = template.Library()


@register.filter
def is_candidate(user):
    return user is not None and user.role is not None and user.role == Role.CANDIDATE


@register.filter
def is_recruiter(user):
    return user is not None and user.role is not None and user.role == Role.RECRUITER
