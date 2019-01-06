import django.contrib

import FuzzEd.models as models


django.contrib.admin.site.register(models.Graph)
django.contrib.admin.site.register(models.Project)
django.contrib.admin.site.register(models.Job)
django.contrib.admin.site.register(models.Notification)
