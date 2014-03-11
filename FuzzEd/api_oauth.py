"""
    This is the API for everybody else beside the frontend. Access restrictions here are managed by OAuth.

    Security: No resource ownership checks ('is this his graph ?') should happen here, 
              only access security ('is he allowed to use that functionality ?').
"""

from FuzzEd.middleware import HttpResponseServerErrorAnswer
from oauth2_provider.views.generic import ProtectedResourceView

from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication   # rely on Django session user information, filled by oauth2_provider
from tastypie.serializers import Serializer
from tastypie import fields
from FuzzEd.models import Project, Graph

import time
import api

class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.filter(deleted=False)
        authentication = SessionAuthentication()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        excludes = ['deleted', 'owner']

    graphs = fields.ToManyField('FuzzEd.api_oauth.GraphResource', 'graphs')

    def get_object_list(self, request):
        return super(ProjectResource, self).get_object_list(request).filter(owner=request.user)

class GraphSerializer(Serializer):
    formats = ['json', 'tex', 'graphml']
    content_types = {
        'json': 'application/json',
        'tex': 'application/text',
        'graphml': 'application/xml'
    }

    def to_tex(self, data, options=None):
        return data.obj.to_tikz()

    def to_graphml(self, data, options=None):
        return data.obj.to_graphml()

class GraphResource(ModelResource):
    class Meta:
        queryset = Graph.objects.filter(deleted=False)
        authentication = SessionAuthentication()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        serializer = GraphSerializer()
        excludes = ['deleted', 'owner', 'read_only']

    project = fields.ToOneField(ProjectResource, 'project')

    def get_object_list(self, request):
        return super(GraphResource, self).get_object_list(request).filter(owner=request.user)

class GraphDirectExportView(ProtectedResourceView):
    """ Base class for API views that export a graph directly, without rendering job. """
    export_format = None
    def get(self, request, *args, **kwargs):
        assert('graph_id' in kwargs)
        graph_id = int(kwargs['graph_id'])
        return api.graph_download(request.user, graph_id, self.export_format)

class GraphJobExportView(ProtectedResourceView):
    """ Base class for API views that export a graph based on a rendering job result. """
    export_format = None
    def get(self, request, *args, **kwargs):
        assert('graph_id' in kwargs)
        graph_id = int(kwargs['graph_id'])
        job = api.job_create(request.user, graph_id, self.export_format)
        while not job.done():
            # TODO: Move this to central settings.ini
            time.sleep(2)
        status, job = api.job_status(request.user, job.pk)
        if status == 0:
            return api.graph_download(request.user, graph_id, self.export_format)
        else:
            raise HttpResponseServerErrorAnswer("Internal error, could not create file. Try the web frontend.")

class GraphEpsExportView(GraphJobExportView):
    export_format = 'eps'

class GraphPdfExportView(GraphJobExportView):
    export_format = 'pdf'

class GraphTexExportView(GraphDirectExportView):
    export_format = 'tex'

class GraphGraphmlExportView(GraphDirectExportView):
    export_format = 'graphml'

