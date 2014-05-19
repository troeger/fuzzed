#from oauth2_provider.views.generic import ProtectedResourceView        see urls.py for further explanation

import logging
logger = logging.getLogger('FuzzEd')

import common

class GraphResource(common.GraphResource):
    class Meta(common.GraphResource.Meta):
        authentication = common.OurApiKeyAuthentication()

class ProjectResource(common.ProjectResource):
    class Meta(common.ProjectResource.Meta):
        authentication = common.OurApiKeyAuthentication()
