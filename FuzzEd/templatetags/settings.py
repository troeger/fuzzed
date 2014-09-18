from django import template
import FuzzEd
register = template.Library()

def setting(name):
	if name == "VERSION":
		return FuzzEd.VERSION
	else:
	    return getattr(FuzzEd.settings, name, "")

register.simple_tag(setting)