from django import template

from job_board.users.constants import Role

register = template.Library()


@register.filter
def is_candidate(user):
    return user is not None and user.role is not None and user.role == Role.CANDIDATE


@register.filter
def is_recruiter(user):
    return user is not None and user.role is not None and user.role == Role.RECRUITER


@register.filter
def cool_number(value, num_decimals=2):
    """
    Django template filter to convert regular numbers to a
    cool format (ie: 2K, 434.4K, 33M...)
    round the numbers to millions, billions etc...
    :param value: number
    :param num_decimals: Number of decimal digits
    """

    int_value = int(value)
    formatted_number = "{{:.{}f}}".format(num_decimals)
    if int_value < 1000:
        return str(int_value)
    elif int_value < 1000000:
        return formatted_number.format(int_value / 1000.0).rstrip("0.") + "K"
    else:
        return formatted_number.format(int_value / 1000000.0).rstrip("0.") + "M"
