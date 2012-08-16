import fuzztrees.models as model
import django.contrib

django.contrib.admin.site.register(model.Graph)
django.contrib.admin.site.register(model.Node)
django.contrib.admin.site.register(model.Edge)
django.contrib.admin.site.register(model.Property)