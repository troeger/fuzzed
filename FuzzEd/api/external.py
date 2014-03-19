"""
    This is the API for everybody else beside the frontend. 
    Access restrictions here are managed by Tastypie's API key.
"""

#from oauth2_provider.views.generic import ProtectedResourceView        see urls.py for further explanation
from FuzzEd.middleware import HttpResponseServerErrorAnswer
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication   
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized, UnsupportedFormat
from tastypie.serializers import Serializer
from tastypie import fields
from FuzzEd.models import Project, Graph

import time

class ProjectResource(ModelResource):
    '''
        An API resource for projects.
    '''
    graphs = fields.ToManyField('FuzzEd.api_ext.GraphResource', 'graphs')

    class Meta:
        queryset = Project.objects.filter(deleted=False)
        authentication = ApiKeyAuthentication()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        excludes = ['deleted', 'owner']
        nested = 'graph'

    def get_object_list(self, request):
        return super(ProjectResource, self).get_object_list(request).filter(owner=request.user)

class GraphSerializer(Serializer):
    """
        Our custom serializer / deserializer for graph formats we support.
        The XML format is GraphML, anything else is not supported.
        The non-implemented deserialization of Tex / JSON input leads to a Tastypie exception,
        which is translated to 401 for the client. There is no explicit way in Tastypie to
        differentiate between supported serialization / deserialization formats.
    """
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

    def from_graphml(self, content):
        ''' 
           Tastypie serialization demands a dictionary of (graph) model
           attribute values here. We return a dummy to support the 
           format officially, and solve the rest in hydrate().
        '''
        return {}

class GraphAuthorization(Authorization):
    '''
        Tastypie authorization class. The main task of this class 
        is to restrict the accessible objects to the ones that the currently
        logged-in user is allowed to use.
    '''
    def read_list(self, object_list, bundle):
        ''' User is only allowed to get the graphs he owns.'''
        return object_list.filter(owner=bundle.request.user)

    def read_detail(self, object_list, bundle):
        ''' User is only allowed to get the graph if he owns it.'''
        return bundle.obj.owner == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.owner == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    def delete_list(self, object_list, bundle):
        return object_list.filter(owner=bundle.request.user)

    def delete_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user


class GraphResource(ModelResource):
    '''
        An API resource for graphs.
    '''
    class Meta:
        queryset = Graph.objects.filter(deleted=False)
        authentication = ApiKeyAuthentication()
        authorization = GraphAuthorization()
        allowed_methods = ['get', 'post']
        serializer = GraphSerializer()
        excludes = ['deleted', 'owner', 'read_only']

    project = fields.ToOneField(ProjectResource, 'project')

    def hydrate(self, bundle):
        # Make sure that owners are assigned correctly
        bundle.obj.owner=bundle.request.user
        # Get the user-specified project, and make sure that it is his.
        # This is not an authorization problem for the (graph) resource itself, 
        # so it must be handled here and not in the auth class.
        try:
            project = Project.objects.get(pk=bundle.request.GET['project'], owner=bundle.request.user)
            bundle.obj.project=project
        except:
            raise Unauthorized("You can't use this project for your new graph.") 
        # Fill the graph with the GraphML data
        bundle.obj.from_graphml(bundle.request.body)     
        return bundle  

# class GraphJobExportView(ProtectedResourceView):
#     """ Base class for API views that export a graph based on a rendering job result. """
#     export_format = None
#     def get(self, request, *args, **kwargs):
#         assert('graph_id' in kwargs)
#         graph_id = int(kwargs['graph_id'])
#         job = api.job_create(request.user, graph_id, self.export_format)
#         while not job.done():
#             # TODO: Move this to central settings.ini
#             time.sleep(2)
#         status, job = api.job_status(request.user, job.pk)
#         if status == 0:
#             return api.graph_download(request.user, graph_id, self.export_format)
#         else:
#             raise HttpResponseServerErrorAnswer("Internal error, could not create file. Try the web frontend.")

