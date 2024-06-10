from django import template
from django.conf import settings
import ore
import os

register = template.Library()


@register.simple_tag
def setting(name):
    if name == "VERSION":
        return ore.VERSION
    elif name == "ADMIN_NAME":
        return settings.ADMINS[0][0]
    elif name == "ADMIN_EMAIL":
        return settings.ADMINS[0][1]
    else:
        return getattr(settings, name, "")


@register.assignment_tag
def get_dev_login():
    return bool(os.environ.get('ORE_DEV_LOGIN', False)) is True or settings.DEBUG is True
