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
    url(r'^editor/', 'fuzztrees.views.editor', name='editor'),
)

urlpatterns += staticfiles_urlpatterns()
