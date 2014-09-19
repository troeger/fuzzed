from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.contrib import admin
from tastypie.api import Api

from FuzzEd.api import external, frontend, backend


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
                       url(r'^$', 'FuzzEd.views.index', name='index'),
                       url(r'^login/$', 'FuzzEd.views.login', name='login'),
                       url(r'^about/$', 'FuzzEd.views.about', name='about'),
                       url(r'^settings/$',
                           'FuzzEd.views.settings',
                           name='settings'),

                       url(r'^editor/(?P<graph_id>\d+)$',
                           'FuzzEd.views.editor',
                           name='editor'),
                       url(r'^snapshot/(?P<graph_id>\d+)$',
                           'FuzzEd.views.snapshot',
                           name='snapshot'),

                       url(r'^projects/$',
                           'FuzzEd.views.projects',
                           name='projects'),
                       url(r'^projects/new/$',
                           'FuzzEd.views.project_new',
                           name='project_new'),
                       url(r'^projects/(?P<project_id>\d+)/$',
                           'FuzzEd.views.project_edit',
                           name='project_edit'),
                       url(r'^projects/(?P<project_id>\d+)/dashboard/$',
                           'FuzzEd.views.dashboard',
                           name='dashboard'),
                       url(
                           r'^projects/(?P<project_id>\d+)/dashboard/new/(?P<kind>\w{1,50})$',
                           'FuzzEd.views.dashboard_new',
                           name='dashboard_new'),
                       url(r'^projects/(?P<project_id>\d+)/dashboard/edit/',
                           'FuzzEd.views.dashboard_edit',
                           name='dashboard_edit'),
                       url(r'^projects/shared_graphs_dashboard',
                           'FuzzEd.views.shared_graphs_dashboard',
                           name='shared_graphs_dashboard'),
                       url(r'^graphs/(?P<graph_id>\d+)/',
                           'FuzzEd.views.graph_settings',
                           name='graph_settings'),

                       url(
                           r'^robots\.txt$',
                           lambda r: HttpResponse(
                               "User-agent: *\nDisallow: /admin/\nDisallow: /dashboard/\nDisallow: /editor/\n",
                               mimetype="text/plain")),

                       # API
                       url(r'^api/',
                           include(v1_api.urls + front_api.urls + back_api.urls)),

                       # Docs Wiki
                       url(r'^docs/', include('djiki.urls')),

                       # For getting OAuth2 authentication support, enable this
                       # Please note that the application and token registration views are not tailored so far
                       # Example client code lives in ./manage.py oauth, but only deals with trusted client authentication
                       # based on the client secret
                       # For end-user applications, we want to have full redirect support for the client, which smells
                       # more like a separate web application
                       # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),


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
