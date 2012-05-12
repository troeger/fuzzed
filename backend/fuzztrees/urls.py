from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'fuzztrees.views.teaser', name='teaser'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'fuzztrees.views.login', name='login'),
    url(r'^logout/', 'fuzztrees.views.logout', name='logout'),
    url(r'^editor/(?P<graph_id>\d+)$', 'fuzztrees.views.editor', name='editor'),
	url(r'^api/graphs/(?P<graph_id>\d+)$','fuzztrees.api.graph', name='graph'),
	url(r'^api/graphs/(?P<graph_id>\d+)/nodes$','fuzztrees.api.nodes', name='nodes'),
	url(r'^api/graphs/(?P<graph_id>\d+)/nodes/(?P<node_id>\d+)$','fuzztrees.api.node', name='node'),
	url(r'^api/graphs/(?P<graph_id>\d+)/redos$','fuzztrees.api.redos', name='redos'),
	url(r'^api/graphs/(?P<graph_id>\d+)/undos$','fuzztrees.api.undos', name='undos'),
)

urlpatterns += staticfiles_urlpatterns()
