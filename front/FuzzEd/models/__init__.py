from django.contrib import auth

# Needed for Django app registries magic model detection
from . import edge
from . import graph
from . import job
from . import node
from . import node_configuration
from . import node_group
from . import notification
from . import project
from . import properties
from . import result
from . import sharing
from . import user

def user_visible_name(user_obj):
    if user_obj.get_full_name():
        return user_obj.get_full_name()
    else:
        return user_obj.get_username()


auth.models.User.add_to_class('visible_name', user_visible_name)
