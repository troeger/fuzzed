import django.contrib

from FuzzEd.models.graph import Graph
from FuzzEd.models.project import Project
from FuzzEd.models.job import Job
from FuzzEd.models.notification import Notification



django.contrib.admin.site.register(Graph)
django.contrib.admin.site.register(Project)
django.contrib.admin.site.register(Job)
django.contrib.admin.site.register(Notification)
