import FuzzEd.models as models
import django.contrib

django.contrib.admin.site.register(models.Graph)
django.contrib.admin.site.register(models.Node)
django.contrib.admin.site.register(models.Edge)
django.contrib.admin.site.register(models.Property)