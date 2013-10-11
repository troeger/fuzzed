from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from FuzzEd.models import Job
from FuzzEd import settings

from django.contrib import admin
admin.autodiscover()

re_uuid = "[0-F]{8}-[0-F]{4}-[0-F]{4}-[0-F]{4}-[0-F]{12}"

urlpatterns = patterns('',
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # web page
    url(r'^$', 'FuzzEd.views.index', name='index'),
    url(r'^login/$', 'FuzzEd.views.login', name='login'),
    url(r'^about/$', 'FuzzEd.views.about', name='about'),    
    url(r'^settings/$', 'FuzzEd.views.settings', name='settings'),    
    url(r'^dashboard/$', 'FuzzEd.views.dashboard', name='dashboard'),
    url(r'^dashboard/new/$', 'FuzzEd.views.dashboard_new', name='dashboard_new'),
    url(r'^dashboard/(?P<graph_id>\d+)/$', 'FuzzEd.views.dashboard_edit', name='dashboard_edit'),
    url(r'^editor/(?P<graph_id>\d+)$', 'FuzzEd.views.editor', name='editor'),
    url(r'^snapshot/(?P<graph_id>\d+)$', 'FuzzEd.views.snapshot', name='snapshot'),

    # API
    # URL design as in: https://github.com/tinkerpop/rexster/wiki/Basic-REST-API

    # graph
    url(r'^api/graphs$','FuzzEd.api.graphs', name='graphs'),
    url(r'^api/graphs/(?P<graph_id>\d+)$', 'FuzzEd.api.graph', name='graph'),
    url(r'^api/graphs/(?P<graph_id>\d+)/transfers$', 'FuzzEd.api.graph_transfers', name='graph_transfers'),
    url(r'^api/graphs/(?P<graph_id>\d+)/graph_download$', 'FuzzEd.api.graph_download', name='graph_download'),

    # node
    url(r'^api/graphs/(?P<graph_id>\d+)/nodes$', 'FuzzEd.api.nodes', name='nodes'),
    url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)$', 'FuzzEd.api.node', name='node'),

    # properties
    url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)/properties$',
        'FuzzEd.api.properties', name='properties'),
    url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)/properties/(?P<key>)$',
        'FuzzEd.api.property', name='property'),

    # edges
    url(r'^api/graphs/(?P<graph_id>\d+)/edges$','FuzzEd.api.edges', name='edges'),
    url(r'^api/graphs/(?P<graph_id>\d+)/edges/(?P<edge_id>\d+)$','FuzzEd.api.edge', name='edge'),

    # undo/redo
    url(r'^api/graphs/(?P<graph_id>\d+)/redos$','FuzzEd.api.redos', name='redos'),
    url(r'^api/graphs/(?P<graph_id>\d+)/undos$','FuzzEd.api.undos', name='undos'),

    # analysis
    url(r'^api/graphs/(?P<graph_id>\d+)/analysis/cutsets$', 
        'FuzzEd.api.job_create', {'job_kind': Job.CUTSETS_JOB}, name='analyze_cutsets'),
    url(r'^api/graphs/(?P<graph_id>\d+)/analysis/topEventProbability$',
        'FuzzEd.api.job_create', {'job_kind': Job.TOP_EVENT_JOB}, name='analyze_top_event_probability'),

    # jobs
    url(r'^api/jobs/(?P<job_id>\d+)$', 'FuzzEd.api.job_status', name='job_status'),
    url(r'^api/jobs/(?P<job_secret>\S+)/files$', 'FuzzEd.api.job_files', name='job_files'),
)
urlpatterns += staticfiles_urlpatterns()
