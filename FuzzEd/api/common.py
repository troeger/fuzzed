import logging
from abc import abstractmethod

from django.conf.urls import url
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.exceptions import UnsupportedFormat, BadRequest, ImmediateHttpResponse
from django.core.exceptions import ValidationError
from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.http import HttpForbidden, HttpBadRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.cache import patch_cache_control, patch_vary_headers

from FuzzEd.models import Project, Graph


logger = logging.getLogger('FuzzEd')

### Resources ###

class JobResource(ModelResource):
    """
        An API resource for jobs.
    """
    pass

class ProjectResource(ModelResource):
    """
        An API resource for projects.
    """

    class Meta:
        queryset = Project.objects.filter(deleted=False)
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        excludes = ['deleted', 'owner']
        nested = 'graph'

    graphs = fields.ToManyField('FuzzEd.api.external.GraphResource', 'graphs')

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
        'graphml': 'application/xml',
    }

    def to_tex(self, data, options=None):
        return data.obj.to_tikz()

    def to_graphml(self, data, options=None):
        return data.obj.to_graphml()

    def from_graphml(self, content):
        '''
           Tastypie serialization demands a dictionary of (graph) model
           attribute values here. We return a dummy to support the
           format officially, and solve the rest in obj_create().
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
        
        if bundle.obj.owner == bundle.request.user:
            return True
        elif bundle.obj.sharings.filter(user = bundle.request.user):
            bundle.obj.read_only = True
            return True
        else:
            return False
                    
    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.owner == bundle.request.user and not bundle.obj.read_only:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user and not bundle.obj.read_only

    def delete_list(self, object_list, bundle):
        return object_list.filter(owner=bundle.request.user)

    def delete_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user


class GraphResource(ModelResource):
    """
        A graph resource with support for nested node / edge / job resources.
    """

    class Meta:
        queryset = Graph.objects.filter(deleted=False)
        authorization = GraphAuthorization()
        serializer = GraphSerializer()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']

        excludes = ['deleted', 'owner', 'read_only']
        filtering = {"kind": ('exact')}

    project = fields.ToOneField(ProjectResource, 'project')

    def prepend_urls(self):
        return [
            url(r'^graphs/(?P<pk>\d+)$',
                self.wrap_view('dispatch_detail'),
                name='graph'),
            url(r'^graphs/$',
                self.wrap_view('dispatch_list'),
                name='graphs'),
            url(r'^graphs/(?P<pk>\d+)/edges/$',
                self.wrap_view('dispatch_edges'),
                name="edges"),
            url(r'^graphs/(?P<pk>\d+)/edges/(?P<client_id>\d+)$',
                self.wrap_view('dispatch_edge'),
                name="edge"),
            url(r'^graphs/(?P<pk>\d+)/nodes/$',
                self.wrap_view('dispatch_nodes'),
                name="nodes"),
            url(r'^graphs/(?P<pk>\d+)/nodes/(?P<client_id>\d+)$',
                self.wrap_view('dispatch_node'),
                name="node"),
            url(r'^graphs/(?P<pk>\d+)/jobs/$',
                self.wrap_view('dispatch_jobs'),
                name="jobs"),
            url(r'^graphs/(?P<pk>\d+)/jobs/(?P<secret>\S+)/results/$',
                self.wrap_view('dispatch_results'),
                name="results"),
            url(r'^graphs/(?P<pk>\d+)/jobs/(?P<secret>\S+)$',
                self.wrap_view('dispatch_job'),
                name="job"),
            url(r'^graphs/(?P<pk>\d+)/nodegroups/$',
                self.wrap_view('dispatch_nodegroups'),
                name="nodegroups"),
            url(r'^graphs/(?P<pk>\d+)/nodegroups/(?P<client_id>\d+)$',
                self.wrap_view('dispatch_nodegroup'),
                name="nodegroup"),
        ]

    def obj_create(self, bundle, **kwargs):
        bundle.obj = self._meta.object_class()
        bundle.obj.owner = bundle.request.user
        # Get the user-specified project, and make sure that it is his.
        # This is not an authorization problem for the (graph) resource itself,
        # so it must be handled here and not in the auth class.
        try:
            project = Project.objects.get(pk=bundle.request.GET['project'], owner=bundle.request.user)
            bundle.obj.project = project
        except:
            raise ImmediateHttpResponse(response=HttpForbidden("You can't use this project for your new graph."))
            # Fill the graph with the GraphML data
        bundle.obj.from_graphml(bundle.request.body)
        return bundle.obj

    @abstractmethod
    def dispatch_edges(self, request, **kwargs):
        pass

    @abstractmethod
    def dispatch_edge(self, request, **kwargs):
        pass

    @abstractmethod
    def dispatch_nodes(self, request, **kwargs):
        pass

    @abstractmethod
    def dispatch_node(self, request, **kwargs):
        pass

    @abstractmethod
    def dispatch_nodegroups(self, request, **kwargs):
        pass

    @abstractmethod
    def dispatch_nodegroup(self, request, **kwargs):
        pass

    @abstractmethod
    def dispatch_jobs(self, request, **kwargs):
        pass

    @abstractmethod
    def dispatch_results(self, request, **kwargs):
        pass

    @abstractmethod
    def dispatch_job(self, request, **kwargs):
        pass

    def hydrate(self, bundle):
        # Make sure that owners are assigned correctly
        bundle.obj.owner = bundle.request.user
        # Get the user-specified project, and make sure that it is his.
        # This is not an authorization problem for the (graph) resource itself,
        # so it must be handled here and not in the auth class.
        try:
            project = Project.objects.get(pk=bundle.request.GET['project'], owner=bundle.request.user)
            bundle.obj.project = project
        except:
            raise ImmediateHttpResponse(response=HttpForbidden("You can't use this project for your new graph."))
            # Fill the graph with the GraphML data
        bundle.obj.from_graphml(bundle.request.body)
        return bundle


    def wrap_view(self, view):
        """
        Wrap the default Tastypie implementation to return custom error codes instead of generic 500's.
        It also takes care of the correct content disposition.
        """

        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            ''' This is a straight copy from the Tastypie sources,
                extended with the 415 generation code. 
            '''
            try:
                callback = getattr(self, view)
                response = callback(request, *args, **kwargs)

                # Our response can vary based on a number of factors, use
                # the cache class to determine what we should ``Vary`` on so
                # caches won't return the wrong (cached) version.
                varies = getattr(self._meta.cache, "varies", [])

                if varies:
                    patch_vary_headers(response, varies)

                if self._meta.cache.cacheable(request, response):
                    if self._meta.cache.cache_control():
                        # If the request is cacheable and we have a
                        # ``Cache-Control`` available then patch the header.
                        patch_cache_control(response, **self._meta.cache.cache_control())

                if request.is_ajax() and not response.has_header("Cache-Control"):
                    # IE excessively caches XMLHttpRequests, so we're disabling
                    # the browser cache here.
                    # See http://www.enhanceie.com/ie/bugs.asp for details.
                    patch_cache_control(response, no_cache=True)

                # Detect result content type and create some meaningful disposition name
                if 'format' in request.GET:
                    if request.GET['format'] == 'graphml':
                        response['Content-Disposition'] = 'attachment; filename=graph.xml'
                    elif request.GET['format'] == 'tex':
                        response['Content-Disposition'] = 'attachment; filename=graph.tex'
                    elif request.GET['format'] == 'json':
                        response['Content-Disposition'] = 'attachment; filename=graph.json'

                return response
            except UnsupportedFormat as e:
                response = HttpResponse()
                response.status_code = 413
                return response
            except (BadRequest, fields.ApiFieldError) as e:
                data = {"error": e.args[0] if getattr(e, 'args') else ''}
                return self.error_response(request, data, response_class=HttpBadRequest)
            except ValidationError as e:
                data = {"error": e.messages}
                return self.error_response(request, data, response_class=HttpBadRequest)
            except Exception as e:
                if hasattr(e, 'response'):
                    return e.response

                # A real, non-expected exception.
                # Handle the case where the full traceback is more helpful
                # than the serialized error.
                if settings.DEBUG and getattr(settings, 'TASTYPIE_FULL_DEBUG', False):
                    raise

                # Re-raise the error to get a proper traceback when the error
                # happend during a test case
                if request.META.get('SERVER_NAME') == 'testserver':
                    raise

                # Rather than re-raising, we're going to things similar to
                # what Django does. The difference is returning a serialized
                # error message.
                return self._handle_500(request, e)

        return wrapper


