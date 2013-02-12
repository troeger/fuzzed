from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse

from django.db import transaction
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# NOTE: it is important to use our custom exceptions!
# 
# REASON: django.http responses are regular returns, transaction.commit_on_success will therefore  
# REASON: always commit changes even if we return errornous responses (400, 404, ...). We can
# REASON: bypass this behaviour by throwing exception that send correct HTTP status to the user 
# REASON: but abort the transaction. The custom exceptions can be found in middleware.py

from FuzzEd.decorators import require_ajax
from FuzzEd.middleware import HttpResponse, HttpResponseNoResponse, HttpResponseBadRequestAnswer, HttpResponseCreated, HttpResponseNotFoundAnswer, HttpResponseServerErrorAnswer
from FuzzEd.models import Graph, Node, notations, commands
from FuzzEd import backend, settings

import logging, json, urllib, urllib2

logger = logging.getLogger('FuzzEd')

try:
    import json
# backwards compatibility with older python versions
except ImportError:
    import simplejson as json

@login_required
@csrf_exempt
#@require_ajax
@require_http_methods(['GET'])
def calc_topevent(request, graph_id):
    """
    Function: calc_topevent
    
    This API handler is responsible for starting an analysis run in the analysis engine.
    It is intended to return immediately with job information for the frontend.
    If the analysis engine cannot start the job (most likely due to broken XML data generated here),
    the view returns HTTP error code 500 to the front-end.
    """
    import pdb; pdb.set_trace()
    g = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    try:
        post_data = urllib.urlencode(g.to_xml())
        post_data = post_data.encode('utf-8')
        result = urllib2.urlopen('%s'%(settings.CALC_TOPEVENT_SERVER), post_data)  
        # If I got 400 from the analyis engine, it means that I messed up the XML
        if result.getcode() == 400:
            raise HttpResponseServerErrorAnswer()
    except:
        # Something went really wrong here
        raise HttpResponseServerErrorAnswer()

    # determine job id from response
    #TODO: Replace this mock with real information from the analysis server
    response = "{'jobid' : 4711, 'num_configurations' : 50, 'num_nodes' : 34000453}"
    info = json.loads(response)
    # store job information for this graph
    j = Job(name=info['jobid'], configurations=info['configurationa'], nodes=info['nodes'], graph=g, kind=Job.TOPEVENT_JOB)
    j.save()

    # return URL for job status information
    response = HttpResponse(status=201) 
    response['Location'] = urlresolvers.reverse('jobstatus', args=[j.pk])
    return response

@login_required
@csrf_exempt
#@require_ajax
@require_http_methods(['GET'])
def jobstatus(request, job_id):
    try:
        j = Job.objects.get(pk=job_id)
        # Prevent cross-checking of jobs by different users
        assert(j.graph.owner == request.user)
    except:
        # Inform the frontend that the job no longer exists
        # TODO: Add reason for cancellation to body as plain text 
        raise HttpResponseNotFoundAnswer()
    # query status from analysis engine, based on job type
    if j.kind == Job.TOPEVENT_JOB:
        try:
            result = urllib2.request.urlopen('%s/%s'%(settings.CALC_TOPEVENT_SERVER, j.name))  
            if result.getcode() == 202:
                # Backend is not finished with this computation
                return HttpResponse(status=202)
            elif result.getcode() == 200:
                # Computation done
                #TODO: Reformulate the result data to JSON for the frontend
                return HttpResponse(result.read())
        except:
            # Something went really wrong here
            raise HttpResponseServerErrorAnswer()

@login_required
@csrf_exempt
@require_ajax
@require_http_methods(['GET', 'POST'])
@transaction.commit_on_success
def graphs(request):
    """
    Function: graphs
    
    This API handler is responsible for all graphes of the user. It operates in two modes: receiving a GET request will return a JSON encoded list of all the graphs of the user. A POST request instead, will create a new graph (requires the below stated parameters) and returns its ID and URI.
    
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
        raise HttpResponseBadRequestAnswer()

    # Should not be reachable, just for error tracing reasons here
    raise HttpResponseServerErrorAnswer()

@login_required
@csrf_exempt
@require_ajax
@require_GET
def graph(request, graph_id):
    """
    Function: graph
    
    The function provides the JSON serialized version of the graph with the provided id given that the graph is owned by the requesting user and it is not marked as deleted.
    
    Request:            GET - /api/graphs/<GRAPH_ID>
    Request Parameters: None
    Response:           200 - <GRAPH_AS_JSON>
    
    Parameters:
     {HTTPRequest} request   - the django request object
     {int}         graph_id  - the id of the graph to be fetched
    
    Returns:
     {HTTPResponse} a django response object
    """
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)

    return HttpResponse(graph.to_json(), 'application/javascript')
    
@login_required
@csrf_exempt
@require_ajax
@require_POST
@transaction.commit_on_success
def nodes(request, graph_id):
    """
    Function: nodes
    
    This function creates a new node in the graph with the provided it. In order to be able to create the node four data items about the node are needed: its kind, its position (x and y coordinate) and an id as assigned by the client (calculated by the client to prevent waiting for round-trip). The response contains the JSON serialized representation of the newly created node and its new location URI.
    
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
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)    
    try:
        kind = POST['kind']
        assert(kind in notations.by_kind[graph.kind]['nodes'])

        command = commands.AddNode.create_from(graph_id=graph_id, node_id=POST['id'], \
                                             kind=kind, x=POST['x'], y=POST['y'])
        command.do()
        node = command.node

        response = HttpResponse(node.to_json(), 'application/javascript', status=201)
        response['Location'] = reverse('node', args=[node.graph.pk, node.pk])
        return response

    # a int conversion of one of the parameters failed or kind is not supported by the graph
    except (ValueError, AssertionError, KeyError):
        raise HttpResponseBadRequestAnswer()

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
        node = get_object_or_404(Node, client_id=node_id, graph__pk=graph_id, deleted=False)
        if request.method == 'POST':
            # Interpret all parameters as json-formatted. This will also correctly parse
            # numerical values like 'x' and 'y'.
            parameters = json.loads(request.POST.get('properties', {}))
            logger.debug("Changing node %s in graph %s to %s"%(str(node_id),str(graph_id),parameters))
            command = commands.ChangeNode.create_from(graph_id, node_id, parameters)
            command.do()
            # return the updated node object
            return HttpResponse(node.to_json(), 'application/javascript', status=204)

        elif request.method == 'DELETE':
            command = commands.DeleteNode.create_from(graph_id, node_id)
            command.do()
            return HttpResponse(status=204)
    except Exception, e:
        logger.error("Exception: "+str(e))


@login_required
@csrf_exempt
@require_ajax
@require_POST
@transaction.commit_on_success
def edges(request, graph_id):
    """
    Function: edges
    
    This API handler creates a new edge in the graph with the given id. The edge links the two nodes 'source' and 'destination' with each other that are provided in the POST body. Additionally, a request to this URL MUST provide an id for this edge that was assigned by the client (no wait for round-trip). The response contains the JSON serialized representation of the new edge and it location URI.
    
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
        command = commands.AddEdge.create_from(graph_id=graph_id, client_id=POST['id'], \
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
        raise HttpResponseNotFoundAnswer()

    # should never happen, just for completeness reasons here
    except MultipleObjectsReturned:
        raise HttpResponseServerErrorAnswer()

@login_required
@csrf_exempt
@require_ajax
@require_http_methods(['DELETE'])
@transaction.commit_on_success
def edge(request, graph_id, edge_id):
    """
    Function: edge
    
    This API handler deletes the edge from the graph using the both provided ids. The id of the edge hereby referes to the previously assigned client side id and NOT the database id. The response to this request does not contain any body.
    
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
        commands.DeleteEdge.create_from(graph_id=graph_id, edge_id=edge_id).do()
        return HttpResponse(status=204)

    except ValueError:
        raise HttpResponseBadRequestAnswer()

    except ObjectDoesNotExist:
        raise HttpResponseNotFoundAnswer()

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
@require_http_methods(["GET", "POST"])
@transaction.commit_on_success
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
@require_http_methods(["GET", "POST"])
@transaction.commit_on_success
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
def cutsets(request, graph_id):
    """
    The function provides all cut sets of the given graph.
    It currently performs the computation (of unknown duration) synchronousely,
    so the client is expected to perform an asynchronous REST call on its own

    API Request:  GET /api/graphs/[graphID]/cutsets, no body
    API Response: JSON body with list of dicts, one dict per cut set, 'nodes' key has list of client_id's value
    """
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    #tree='(b or c or a) and (c or a and b) and (d) or (e)'
    # minbool is NP-complete, so more than 10 basic events are not feasible for computation
    nodecount = graph.nodes.all().filter(kind__exact="basicEvent", deleted__exact=False).count()
    if nodecount >= 10:
        raise HttpResponseServerErrorAnswer()
    result=backend.getcutsets(graph.to_bool_term())
    #TODO: check the command stack if meanwhile the graph was modified
    return HttpResponse(json.dumps(result), 'application/javascript')
