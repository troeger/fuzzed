from django import template
import FuzzEd
register = template.Library()

def setting(name):
    return getattr(FuzzEd.settings, name, "")

register.simple_tag(setting)