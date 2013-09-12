from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.cache import never_cache

# NOTE: it is important to use our custom exceptions!
# 
# REASON: django.http responses are regular returns, transaction.commit_on_success will therefore  
# REASON: always commit changes even if we return erroneous responses (400, 404, ...). We can
# REASON: bypass this behaviour by throwing exception that send correct HTTP status to the user 
# REASON: but abort the transaction. The custom exceptions can be found in middleware.py

from FuzzEd.decorators import require_ajax
from FuzzEd.middleware import HttpResponse, HttpResponseNoResponse, HttpResponseBadRequestAnswer, \
                              HttpResponseForbiddenAnswer, HttpResponseCreated, HttpResponseNotFoundAnswer, \
                              HttpResponseServerErrorAnswer
from FuzzEd.models import Graph, Node, notations, commands, Job
from analysis import cutsets, top_event_probability
from rendering import renderClient

import logging, json
logger = logging.getLogger('FuzzEd')

@login_required
@csrf_exempt
@require_ajax
@require_http_methods(['GET', 'POST'])
@transaction.commit_on_success
@never_cache
def graphs(request):
    """
    Function: graphs
    
    This API handler is responsible for all graphes of the user. It operates in two modes: receiving a GET request will
    return a JSON encoded list of all the graphs of the user. A POST request instead, will create a new graph (requires
    the below stated parameters) and returns its ID and URI.
    
    Request:            GET - /api/graphs
    Request Parameters: None
    Response:           200 - <GRAPHS_AS_JSON>
                               
    Request:            POST - /api/graphs
    Request Parameters: kind = <GRAPH_KIND>, name = <GRAPH_NAME>
    Response:           201 - Location = <GRAPH_URI>, ID = <GRAPH_ID>
    
    Parameters:
     {HTTPRequest} request  - django request object
                              
    Returns:
     {HTTPResponse} a django response object
    """
    # the user is asking for all of its graphs
    if request.method == 'GET':
        graphs      = Graph.objects.filter(owner=request.user, deleted=False)
        json_graphs = {
            'graphs': [graph.to_dict() for graph in graphs]
        }

        return HttpResponse(json.dumps(json_graphs), 'application/javascript')

    # the request was a post, we are asked to create a new graph
    try:
        # create a graph created command 
        post = request.POST
        command = commands.AddGraph.create_from(kind=post['kind'], name=post['name'], owner=request.user)
        command.do()

        # prepare the response
        graph_id             = command.graph.pk
        response             = HttpResponseCreated()
        response['Location'] = reverse('graph', args=[graph_id])
        response['ID']       = graph_id

        return response

    # something was not right with the request parameters
    except (ValueError, KeyError):
        raise HttpResponseBadRequestAnswer('Bad request parameters.')

@login_required
@csrf_exempt
@require_ajax
@require_GET
@never_cache
def graph(request, graph_id):
    """
    Function: graph
    
    The function provides the JSON serialized version of the graph with the provided id given that the graph is owned
    by the requesting user and it is not marked as deleted.
    
    Request:            GET - /api/graphs/<GRAPH_ID>
    Request Parameters: None
    Response:           200 - <GRAPH_AS_JSON>
    
    Parameters:
     {HTTPRequest} request   - the django request object
     {int}         graph_id  - the id of the graph to be fetched
    
    Returns:
     {HTTPResponse} a django response object
    """
    if request.user.is_staff:
        graph = get_object_or_404(Graph, pk=graph_id)
    else:
        graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)

    return HttpResponse(graph.to_json(), 'application/javascript')

@login_required
@csrf_exempt
@require_GET
def graph_download(request, graph_id):
    """
    Function: graph_download
        Downloads the graph represented in the specified format

    Request:            GET - /api/graphs/<GRAPH_ID>/graph_download
    Request Parameters: [optional] format - Specifies the download format. Default is 'xml'.
    Response:           TODO

    Parameters:
     {HTTPRequest} request   - the django request object
     {int}         graph_id  - the id of the graph to be downloaded

    Returns:
     {HTTPResponse} a django response object
    """
    if request.user.is_staff:
        graph = get_object_or_404(Graph, pk=graph_id)
    else:
        graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)        
    export_format = request.GET.get('format', 'xml')

    response = HttpResponse()

    if export_format == 'xml':
        response.content = graph.to_xml()
        response['Content-Type'] = 'application/xml'

    elif export_format == 'json':
        response.content = graph.to_json()
        response['Content-Type'] = 'application/javascript'
    elif export_format == 'pdf':
        response.content = renderClient.latex2pdf(graph.to_tikz())
        response['Content-Type'] = 'application/pdf'
    elif export_format == 'eps':
        response.content = renderClient.latex2eps(graph.to_tikz())
        response['Content-Type'] = 'application/eps'
    elif export_format == 'tex':
        response.content = graph.to_tikz()
        response['Content-Type'] = 'application/text'
    else:
        raise HttpResponseNotFoundAnswer()

    response['Content-Disposition'] = 'attachment; filename=%s.%s' % (graph.name, export_format)

    return response

@login_required
@csrf_exempt
@require_ajax
@require_GET
def graph_transfers(request, graph_id):
    """
    Function: graph_transfers

    Returns a list of transfers for the given graph

    Request:            GET - /api/graphs/<GRAPH_ID>/transfers
    Request Parameters: graph_id = <INT>
    Response:           200 - <TRANSFERS_AS_JSON>

    Parameters:
     {HTTPRequest} request  - the django request object
     {int}         graph_id - the id of the graph to get the transfers for

    Returns:
     {HTTPResponse} a django response object
    """
    transfers = []
    if request.user.is_staff:
        graph     = get_object_or_404(Graph, pk=graph_id)
    else:
        graph     = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)        

    if graph.kind in ['faulttree', 'fuzztree']:
        for transfer in Graph.objects.filter(~Q(pk=graph_id), owner=request.user, kind=graph.kind, deleted=False):
            transfers.append({'id': transfer.pk, 'name': transfer.name})

    return HttpResponse(json.dumps({'transfers': transfers}), 'application/javascript', status=200)

@login_required
@csrf_exempt
@require_ajax
@require_POST
@transaction.commit_on_success
@never_cache
def nodes(request, graph_id):
    """
    Function: nodes
    
    This function creates a new node in the graph with the provided it. In order to be able to create the node four data
    items about the node are needed: its kind, its position (x and y coordinate) and an id as assigned by the client
    (calculated by the client to prevent waiting for round-trip). The response contains the JSON serialized
    representation of the newly created node and its new location URI.
    
    Request:            POST - /api/graphs/<GRAPH_ID>/nodes
    Request Parameters: client_id = <INT>, kind = <NODE_TYPE>, x = <INT>, y = <INT>
    Response:           201 - <NODE_AS_JSON>, Location = <NODE_URI>
    
    Parameters:
     {HTTPRequest} request   - the django request object
     {int}         graph_id  - the id of the graph where the node shall be added
    
    Returns:
     {HTTPResponse} a django response object
    """
    POST = request.POST
    if request.user.is_staff:
        graph = get_object_or_404(Graph, pk=graph_id)
    else:
        graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    try:
        if graph.read_only:
            raise HttpResponseForbiddenAnswer('Trying to create a node in a read-only graph')

        kind = POST['kind']
        assert(kind in notations.by_kind[graph.kind]['nodes'])

        command = commands.AddNode.create_from(graph_id=graph_id, node_id=POST['id'],
                                               kind=kind, x=POST['x'], y=POST['y'])
        command.do()
        node = command.node

        response = HttpResponse(node.to_json(), 'application/javascript', status=201)
        response['Location'] = reverse('node', args=[node.graph.pk, node.pk])
        return response

    # a int conversion of one of the parameters failed or kind is not supported by the graph
    except (ValueError, AssertionError, KeyError):
        raise HttpResponseBadRequestAnswer("Bad arguments in the request.")

    # the looked up graph does not exist
    except ObjectDoesNotExist:
        raise HttpResponseNotFoundAnswer()

    # should never happen, but for completeness enlisted here
    except MultipleObjectsReturned:
        raise HttpResponseServerErrorAnswer()

@login_required
@csrf_exempt
@require_ajax
@require_http_methods(['DELETE', 'POST'])
@transaction.commit_on_success
@never_cache
def node(request, graph_id, node_id):
    """
    Function: node
        API handler for all actions on one specific node. This includes changing attributes of a node
        or deleting it.

        Request:            POST - /api/graphs/<GRAPH_ID>/nodes/<NODE_ID>
        Request Parameters: any key-value pairs of attributes that should be changed
        Response:           204 - JSON representation of the node

        Request:            DELETE - /api/graphs/<GRAPH_ID>/nodes/<NODE_ID>
        Request Parameters: none
        Response:           204

    Parameters:
        {HTTPRequest} request   - the django request object
        {int}         graph_id  - the id of the graph where the edge shall be added
        {int}         node_id   - the id of the node that should be changed/deleted

    Returns:
        {HTTPResponse} a django response object
    """
    try:
        node = get_object_or_404(Node, client_id=node_id, graph__pk=graph_id)

        if node.graph.read_only:
            raise HttpResponseForbiddenAnswer('Trying to modify a node in a read-only graph')

        if request.method == 'POST':
            # Interpret all parameters as json. This will ensure correct parsing of numerical values like e.g. ids
            parameters = json.loads(request.POST.get('properties', {}))

            logger.debug('Changing node %s in graph %s to %s' % (node_id, graph_id, parameters))
            command = commands.ChangeNode.create_from(graph_id, node_id, parameters)
            command.do()

            # return the updated node object
            return HttpResponse(node.to_json(), 'application/javascript', status=204)

        elif request.method == 'DELETE':
            command = commands.DeleteNode.create_from(graph_id, node_id)
            command.do()
            return HttpResponse(status=204)

    except Exception as exception:
        logger.error('Exception: ' + str(exception))
        raise exception

@login_required
@csrf_exempt
@require_ajax
@require_POST
@transaction.commit_on_success
@never_cache
def edges(request, graph_id):
    """
    Function: edges
    
    This API handler creates a new edge in the graph with the given id. The edge links the two nodes 'source' and
    'destination' with each other that are provided in the POST body. Additionally, a request to this URL MUST provide
    an id for this edge that was assigned by the client (no wait for round-trip). The response contains the JSON
    serialized representation of the new edge and it location URI.
    
    Request:            POST - /api/graphs/<GRAPH_ID>/edges
    Request Parameters: client_id = <INT>, source = <INT>, destination = <INT>
    Response:           201 - <EDGE_AS_JSON>, Location = <EDGE_URI>
    
    Parameters:
     {HTTPRequest} request   - the django request object
     {int}         graph_id  - the id of the graph where the edge shall be added
    
    Returns:
     {HTTPResponse} a django response object
    """
    POST = request.POST
    try:
        if request.user.is_staff:
            graph = get_object_or_404(Graph, pk=graph_id)
        else:
            graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
        if graph.read_only:
            raise HttpResponseForbiddenAnswer('Trying to create an edge in a read-only graph')

        command = commands.AddEdge.create_from(graph_id=graph_id, client_id=POST['id'],
                                               from_id=POST['source'], to_id=POST['destination'])
        command.do()

        edge = command.edge
        response = HttpResponse(edge.to_json(), 'application/javascript', status=201)
        response['Location'] = reverse('edge', kwargs={'graph_id': graph_id, 'edge_id': edge.client_id})

        return response

    # some values in the request were not parsable
    except (ValueError, KeyError):
        raise HttpResponseBadRequestAnswer()

    # either the graph, the source or the destination node are not in the database
    except ObjectDoesNotExist:
        raise HttpResponseNotFoundAnswer("Invalid graph or node ID")

    # should never happen, just for completeness reasons here
    except MultipleObjectsReturned:
        raise HttpResponseServerErrorAnswer()

@login_required
@csrf_exempt
@require_ajax
@require_http_methods(['DELETE'])
@transaction.commit_on_success
@never_cache
def edge(request, graph_id, edge_id):
    """
    Function: edge
    
    This API handler deletes the edge from the graph using the both provided ids. The id of the edge hereby refers to
    the previously assigned client side id and NOT the database id. The response to this request does not contain any
    body.
    
    Request:            DELETE - /api/graphs/<GRAPH_ID>/edge/<EDGE_ID>
    Request Parameters: None
    Response:           204
    
    Parameters:
     {HTTPRequest} request   - the django request object
     {int}         graph_id  - the id of the graph where the edge shall be deleted
     {int}         edge_id   - the id of the edge to be deleted
    
    Returns:
     {HTTPResponse} a django response object
    """
    try:
        if request.user.is_staff:
            graph = get_object_or_404(Graph, pk=graph_id)
        else:
            graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)            
        if graph.read_only:
            raise HttpResponseForbiddenAnswer('Trying to delete an edge in a read-only graph')

        commands.DeleteEdge.create_from(graph_id=graph_id, edge_id=edge_id).do()
        return HttpResponse(status=204)

    except ValueError:
        raise HttpResponseBadRequestAnswer()

    except ObjectDoesNotExist:
        raise HttpResponseNotFoundAnswer("Invalid edge ID")

    except MultipleObjectsReturned:
        raise HttpResponseServerErrorAnswer()

# TODO: PROVIDE ALL PROPERTIES OF A NODE (/nodes/<id>/properties)
def properties(**kwargs):
    pass

# TODO: PROVIDE THE VALUE OF A PROPERTY WITH GIVEN KEY (/nodes/<id>/properties/<key>)
def property(**kwargs):
    pass

@login_required
@csrf_exempt
@require_ajax
@require_http_methods(['GET', 'POST'])
@transaction.commit_on_success
@never_cache
def undos(request, graph_id):
    #
    # TODO: IS NOT WORKING YET
    # TODO: UPDATE DOC STRING
    #
    """
    Fetch undo command stack from backend
    API Request:  GET /api/graphs/[graphID]/undos, no body
    API Response: JSON body with command array of undo stack

    Tell the backend that an undo has been issued in the model
    API Request:  POST /api/graphs/[graphID]/undos, no body
    API Response: no body, status code 204
    """
    if request.method == 'GET':
        #TODO: Fetch undo stack for the graph
        return HttpResponseNoResponse()
        
    else:
        #TODO: Perform top command on undo stack
        return HttpResponseNoResponse()

@login_required
@csrf_exempt
@require_ajax
@require_http_methods(['GET', 'POST'])
@transaction.commit_on_success
@never_cache
def redos(request, graph_id):
    #
    # TODO: IS NOT WORKING YET
    # TODO: UPDATE DOC STRING
    #
    """
    Fetch redo command stack from backend
    API Request:  GET /api/graphs/[graphID]/redos, no body
    API Response: JSON body with command array of redo stack

    Tell the backend that an redo has been issued in the model
    API Request:  POST /api/graphs/[graphID]/redos, no body
    API Response: no body, status code 204
    """
    if request.method == 'GET':
        #TODO Fetch redo stack for the graph
        return HttpResponseNoResponse()
    else:
        #TODO Perform top command on redo stack
        return HttpResponseNoResponse()

@login_required
@csrf_exempt
@require_ajax
@require_GET
@transaction.commit_on_success
@never_cache
def analyze_cutsets(request, graph_id):
    """
    The function provides all cut sets of the given graph.
    It currently performs the computation (of unknown duration) synchronously,
    so the client is expected to perform an asynchronous REST call on its own

    API Request:  GET /api/graphs/[graphID]/cutsets, no body
    API Response: JSON body with list of dicts, one dict per cut set, 'nodes' key has list of client_id's value
    """
    if request.user.is_staff:
        graph = get_object_or_404(Graph, pk=graph_id)
    else:
        graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    # minbool is NP-complete, so more than 10 basic events are not feasible for computation
    node_count = graph.nodes.all().filter(kind__exact='basicEvent', deleted__exact=False).count()

    if node_count >= 10:
        raise HttpResponseServerErrorAnswer()

    result = cutsets.get(graph.to_bool_term())
    #TODO: check the command stack if meanwhile the graph was modified
    return HttpResponse(json.dumps(result), 'application/javascript')

@login_required
@csrf_exempt
@require_http_methods(['GET'])
def analyze_top_event_probability(request, graph_id):
    """
    Function: analyze_top_event_probability

    This API handler is responsible for starting an analysis run in the analysis engine.
    It is intended to return immediately with job information for the frontend.
    If the analysis engine cannot start the job (most likely due to broken XML data generated here),
    the view returns HttpResponseServerErrorAnswer to the front-end.
    """
    if request.user.is_staff:
        graph = get_object_or_404(Graph, pk=graph_id)
    else:
        graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)

    try:
        # The Java analysis server currently only likes FuzzTree XML
        post_data = graph.to_xml('fuzztree')
        # Determine stored decomposition number
        decompNumber = graph.top_node().get_property('decompositions')
        logger.debug('Decomposition number of this graph is '+str(decompNumber))
        logger.debug('Sending XML to analysis server:\n' + post_data)
        job_id, configuration_count, node_count = top_event_probability.create_job(post_data,decompNumber)

        # store job information for this graph
        job = Job(name=job_id, configurations=configuration_count,
                  nodes=node_count, graph=graph, kind=Job.TOP_EVENT_JOB)
        job.save()

        # return URL for job status information
        logger.debug('Got new job \'%s\' with ID %d for graph %d' % (job.name, job.pk, graph.pk))
        response = HttpResponse(status=201)
        response['Location'] = reverse('job_status', args=[job.pk])

        return response

    except top_event_probability.InternalError as exception:
        logger.error('Exception while using analysis server: %s' % str(exception))
        #TODO: Perform some smarter error handling here
        raise HttpResponseServerErrorAnswer(str(exception))

@login_required
@csrf_exempt
@require_http_methods(['GET'])
def job_status(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        # Prevent cross-checking of jobs by different users
        assert(job.graph.owner == request.user or request.user.is_staff)

    except:
        # Inform the frontend that the job no longer exists
        # TODO: Add reason for cancellation to body as plain text
        raise HttpResponseNotFoundAnswer()

    if job.kind != Job.TOP_EVENT_JOB:
        raise HttpResponseBadRequestAnswer()

    # query status from analysis engine, based on job type
    try:
        result = top_event_probability.get_job_result(job.name)

        if result is None:
            return HttpResponse(status=202)

        else:
            logger.debug('Analysis result:\n%s' % result)
            return HttpResponse(result)

    except Exception as exception:
        # Analysis engine does not know this job, or something else went wrong
        # for the frontend, this is basically an unspecified backend error
        logger.error('Error while fetching analysis server job status: %s' % exception)
        raise HttpResponseServerErrorAnswer()
