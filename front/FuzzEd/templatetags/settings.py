from django import template
import FuzzEd
from FuzzEd import settings
register = template.Library()


@register.simple_tag
def setting(name):
    if name == "VERSION":
        return FuzzEd.VERSION
    else:
        return getattr(FuzzEd.settings, name, "")


@register.assignment_tag
def get_debug_status():
    return settings.DEBUG is True
