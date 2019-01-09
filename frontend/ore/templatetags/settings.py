from django import template
from django.conf import settings
import ore

register = template.Library()


@register.simple_tag
def setting(name):
    if name == "VERSION":
        return ore.VERSION
    else:
        return getattr(settings, name, "")


@register.assignment_tag
def get_debug_status():
    return settings.DEBUG is True
