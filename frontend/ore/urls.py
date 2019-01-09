from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from tastypie.api import Api

from ore.api import external, frontend, backend


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

urlpatterns = patterns('',
                       # admin
                       url(r'^admin/doc/',
                           include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),

                       # Django Frontend Views
                       url(r'^$', 'ore.views.index', name='index'),
                       url(r'^login/$', 'ore.views.login', name='login'),
                       url(r'^about/$', 'ore.views.about', name='about'),
                       url(r'^settings/$',
                           'ore.views.settings',
                           name='settings'),

                       url(r'^editor/(?P<graph_id>\d+)$',
                           'ore.views.editor',
                           name='editor'),
                       url(r'^snapshot/(?P<graph_id>\d+)$',
                           'ore.views.snapshot',
                           name='snapshot'),

                       url(r'^projects/$',
                           'ore.views.projects',
                           name='projects'),
                       url(r'^projects/new/$',
                           'ore.views.project_new',
                           name='project_new'),
                       url(r'^projects/(?P<project_id>\d+)/$',
                           'ore.views.project_edit',
                           name='project_edit'),
                       url(r'^projects/(?P<project_id>\d+)/dashboard/$',
                           'ore.views.dashboard',
                           name='dashboard'),
                       url(
                           r'^projects/(?P<project_id>\d+)/dashboard/new/(?P<kind>\w{1,50})$',
                           'ore.views.dashboard_new',
                           name='dashboard_new'),
                       url(r'^projects/(?P<project_id>\d+)/dashboard/import/',
                           'ore.views.dashboard_import',
                           name='dashboard_import'),
                       url(r'^projects/(?P<project_id>\d+)/dashboard/edit/',
                           'ore.views.dashboard_edit',
                           name='dashboard_edit'),
                       url(r'^projects/shared_graphs_dashboard',
                           'ore.views.shared_graphs_dashboard',
                           name='shared_graphs_dashboard'),
                       url(r'^graphs/(?P<graph_id>\d+)/',
                           'ore.views.graph_settings',
                           name='graph_settings'),

                       # robots.txt via django-robots
                       url(r'^robots\.txt$', include('robots.urls')),

                       # API
                       url(r'^api/',
                           include(v1_api.urls + front_api.urls + back_api.urls)),

                       # Django Social Auth
                       url(r'', include('social.apps.django_app.urls', namespace='social'))

                       )
urlpatterns += staticfiles_urlpatterns()

# Some debugging code that shows the final complete list of all configured
# URL's


def show_urls(urllist, depth=0):
    for entry in urllist:
        print "  " * depth, entry.regex.pattern
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)
# show_urls(urlpatterns)
