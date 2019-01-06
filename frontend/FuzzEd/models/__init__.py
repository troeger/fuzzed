from django.contrib import auth

from .project import Project
from .graph import Graph
from .sharing import Sharing
from .node import Node
from .edge import Edge
from .job import Job
from .properties import Property
from .user import UserProfile
from .result import Result
from .configuration import Configuration
from .node_configuration import NodeConfiguration
#from machine import Machine
from .notification import Notification
from .node_group import NodeGroup


def user_visible_name(user_obj):
    if user_obj.get_full_name():
        return user_obj.get_full_name()
    else:
        return user_obj.get_username()

auth.models.User.add_to_class('visible_name', user_visible_name)
