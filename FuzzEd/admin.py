import FuzzEd.models as models
import django.contrib

django.contrib.admin.site.register(models.Graph)
django.contrib.admin.site.register(models.Project)
django.contrib.admin.site.register(models.Notification)
