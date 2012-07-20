from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'fuzztrees.views.index', name='index'),
	url(r'^admin/doc/$', include('django.contrib.admindocs.urls')),
	url(r'^admin/$', include(admin.site.urls)),
	url(r'^login/$', 'fuzztrees.views.login', name='login'),
	url(r'^about/$', 'fuzztrees.views.about', name='about'),    
	url(r'^settings/$', 'fuzztrees.views.settings', name='settings'),    
	url(r'^dashboard/$', 'fuzztrees.views.dashboard', name='dashboard'),
	url(r'^dashboard/new/$', 'fuzztrees.views.dashboard_new', name='dashboard_new'),
	url(r'^dashboard/(?P<graph_id>\d+)/$', 'fuzztrees.views.dashboard_edit', name='dashboard_edit'),
	url(r'^editor/(?P<graph_id>\d+)$', 'fuzztrees.views.editor', name='editor'),
	url(r'^api/graphs$','fuzztrees.api.graphs', name='graphs'),
	url(r'^api/graphs/(?P<graph_id>\d+)$','fuzztrees.api.graph', name='graph'),
	url(r'^api/graphs/(?P<graph_id>\d+)/nodes$','fuzztrees.api.nodes', name='nodes'),
	url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)$','fuzztrees.api.node', name='node'),
	url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)/edges$','fuzztrees.api.edges', name='edges'),
	url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)/edges/(?P<edge_id>\d+)$','fuzztrees.api.edge', name='edge'),
	url(r'^api/graphs/(?P<graph_id>\d+)/redos$','fuzztrees.api.redos', name='redos'),
	url(r'^api/graphs/(?P<graph_id>\d+)/undos$','fuzztrees.api.undos', name='undos')
)

urlpatterns += staticfiles_urlpatterns()