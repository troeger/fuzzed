from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

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

    # API
    # URL design as in: https://github.com/tinkerpop/rexster/wiki/Basic-REST-API
    url(r'^api/graphs$','FuzzEd.api.graphs', name='graphs'),
    url(r'^api/graphs/(?P<graph_id>\d+)$', 'FuzzEd.api.graph', name='graph'),

    url(r'^api/graphs/(?P<graph_id>\d+)/download$', 'FuzzEd.api.download', name='download'),

    url(r'^api/graphs/(?P<graph_id>\d+)/nodes$', 'FuzzEd.api.nodes', name='nodes'),
    url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)$', 'FuzzEd.api.node', name='node'),

    url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)/properties$', \
        'FuzzEd.api.properties', name='properties'),
    url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)/properties/(?P<key>)$', \
        'FuzzEd.api.property', name='property'),

    url(r'^api/graphs/(?P<graph_id>\d+)/edges$','FuzzEd.api.edges', name='edges'),
    url(r'^api/graphs/(?P<graph_id>\d+)/edges/(?P<edge_id>\d+)$','FuzzEd.api.edge', name='edge'),

    url(r'^api/graphs/(?P<graph_id>\d+)/redos$','FuzzEd.api.redos', name='redos'),
    url(r'^api/graphs/(?P<graph_id>\d+)/undos$','FuzzEd.api.undos', name='undos'),

    url(r'^api/graphs/(?P<graph_id>\d+)/cutsets$', 'FuzzEd.api.cutsets', name='cutsets'),

    url(r'^api/graphs/(?P<graph_id>\d+)/calc/topevent$', 'FuzzEd.api.calc_topevent'),
    url(r'^api/jobs/(?P<job_id>\d+)$', 'FuzzEd.api.jobstatus', name='jobstatus'),
)

urlpatterns += staticfiles_urlpatterns()