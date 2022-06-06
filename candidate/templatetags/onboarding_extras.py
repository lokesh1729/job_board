from django.template.defaultfilters import register


@register.filter(name="concat_hyphen")
def concat_hyphen(value, arg):
    return f"{value}--{arg}"


@register.filter(name="get_value")
def get_value_from_object(attr, obj):
    if hasattr(obj, attr):
        return getattr(obj, attr)
    if isinstance(obj, dict) and attr in obj:
        return obj[attr]
    return None
