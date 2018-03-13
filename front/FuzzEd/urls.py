from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from tastypie.api import Api

from FuzzEd.api import external, frontend, backend
from FuzzEd import views


v1_api = Api(api_name='v1')
v1_api.register(external.ProjectResource())
v1_api.register(external.GraphResource())
front_api = Api(api_name='front')
front_api.register(frontend.ProjectResource())
front_api.register(frontend.GraphResource())
front_api.register(frontend.EdgeResource())
front_api.register(frontend.NodeResource())
front_api.register(frontend.NodeGroupResource())
front_api.register(frontend.NotificationResource())
front_api.register(frontend.JobResource())
front_api.register(frontend.ResultResource())
back_api = Api(api_name='back')
back_api.register(backend.JobResource())

admin.autodiscover()

re_uuid = "[0-F]{8}-[0-F]{4}-[0-F]{4}-[0-F]{4}-[0-F]{12}"

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^about/$', views.about, name='about'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^editor/(?P<graph_id>\d+)$', views.editor, name='editor'),
    url(r'^snapshot/(?P<graph_id>\d+)$', views.snapshot, name='snapshot'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/new/$', views.project_new, name='project_new'),
    url(r'^projects/(?P<project_id>\d+)/$', views.project_edit, name='project_edit'),
    url(r'^projects/(?P<project_id>\d+)/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^projects/(?P<project_id>\d+)/dashboard/new/(?P<kind>\w{1,50})$', views.dashboard_new, name='dashboard_new'),
    url(r'^projects/(?P<project_id>\d+)/dashboard/import/', views.dashboard_import, name='dashboard_import'),
    url(r'^projects/(?P<project_id>\d+)/dashboard/edit/', views.dashboard_edit, name='dashboard_edit'),
    url(r'^projects/shared_graphs_dashboard', views.shared_graphs_dashboard, name='shared_graphs_dashboard'),
    url(r'^graphs/(?P<graph_id>\d+)/', views.graph_settings, name='graph_settings'),
    url(r'^robots\.txt', include('robots.urls')),
    url(r'^api/', include(v1_api.urls + front_api.urls + back_api.urls)),
    url(r'', include('social_django.urls', namespace='social'))
]

urlpatterns += staticfiles_urlpatterns()

