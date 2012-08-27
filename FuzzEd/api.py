from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse

from django.db import transaction

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# NOTE: it is important to use our custom exceptions!
# REASON: transaction.commit_on_success will always commit if we do not throw an exception
# REASON: django.http however is a regular return
from FuzzEd.middleware import HttpResponseBadRequestAnswer, HttpResponseNotFoundAnswer, HttpResponseServerErrorAnswer
from FuzzEd.models import Graph, Node, Edge, notations, commands

import logging
logger = logging.getLogger('FuzzEd')

@login_required
@require_POST
@csrf_exempt
@transaction.commit_on_success
def graphs(request):
    """
    Function: graphs
    
    This function is the API call handler for requests to create a new graph. The request structure must be as follows:
    
    Request:            POST - /api/graphs
    Request Parameters: kind = <GRAPH_KIND>, name = <GRAPH_NAME>
    Response:           201 - Location = <GRAPH_URI>, ID = <GRAPH_ID>
    
    Parameters:
     {HTTPRequest} request  - django request object
                              
    Returns:
     {HTTPResponse} a django response object
    """ 
    # we do not accept non AJAX requests
    if not request.is_ajax():
        raise HttpResponseBadRequestAnswer()

    # try to create the graph like we normally would
    try:
        # create a graph created command 
        post    = request.POST
        commands.AddGraph.create_of(kind=post['kind'], name=post['name'], \
                                    owner=request.user, undoable=False).do()

        # prepare the response
        graph_id             = command.graph.pk
        response             = HttpResponseCreated()
        response['Location'] = reverse('graph', args=[graph_id])
        response['ID']       = graph_id

        return response

    # something was not right with the request parameters
    except ValueError, KeyError:
        raise HttpResponseBadRequestAnswer()

    # Should not be reachable, just for error tracing reasons here
    raise HttpResponseServerErrorAnswer()

@login_required
@require_GET
@csrf_exempt
def graph(request, graph_id):
    """
    Function: graph
    
    The function provides the JSON serialized version of the graph with the given id given that the graph is owned by the requesting user and it is not marked as deleted.
    
    Request:            GET - /api/graphs/<GRAPH_ID>
    Request Parameters: None
    Response:           200 - <GRAPH_AS_JSON>
    
    Parameters:
     {HTTPRequest} request   - the django request object
     {int}         graph_id  - the id of the graph to be fetched
    
    Returns:
     {HTTPResponse} a django response object
    """
    # only AJAX requests are permitted...
    if not request.is_ajax():
        raise HttpResponseBadRequestAnswer()
    
    # fetch graph and write back JSON-serialized representation
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    return HttpResponse(graph.to_json(), 'application/javascript')

@login_required
@require_http_methods(["GET", "POST"])
@csrf_exempt
@transaction.commit_on_success
def undos(request, graph_id):
    #
    # TODO: IS NOT WORKING YET
    #
    """
    Fetch undo command stack from backend
    API Request:  GET /api/graphs/[graphID]/undos, no body
    API Response: JSON body with command array of undo stack

    Tell the backend that an undo has been issued in the model
    API Request:  POST /api/graphs/[graphID]/undos, no body
    API Response: no body, status code 204
    """
    if not request.is_ajax():
        raise HttpResponseBadRequestAnswer()

    if request.method == 'GET':
        #TODO: Fetch undo stack for the graph
        raise HttpResponseNoResponseAnswer()
        
    else:
        #TODO: Perform top command on undo stack
        raise HttpResponseNoResponseAnswer()

@login_required
@require_http_methods(["GET", "POST"])
@csrf_exempt
@transaction.commit_on_success
def redos(request, graph_id):
    #
    # TODO: IS NOT WORKING YET
    #
    """
    Fetch redo command stack from backend
    API Request:  GET /api/graphs/[graphID]/redos, no body
    API Response: JSON body with command array of redo stack

    Tell the backend that an redo has been issued in the model
    API Request:  POST /api/graphs/[graphID]/redos, no body
    API Response: no body, status code 204
    """
    if not request.is_ajax():
        raise HttpResponseBadRequestAnswer()

    if request.method == 'GET':
        #TODO Fetch redo stack for the graph
        raise HttpResponseNoResponseAnswer()
    else:
        #TODO Perform top command on redo stack
        raise HttpResponseNoResponseAnswer()
    
@login_required
@require_POST
@csrf_exempt
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
    # we do not accept non-AJAX requests
    if not request.is_ajax():
        raise HttpResponseBadRequestAnswer()

    POST = request.POST
    # if client_id, kind, x or y is not provided we are not able to create the node
    if not POST.get('client_id') or not POST.get('kind') or not POST.get('x') or not POST.get('y'):
        raise HttpResponseBadRequestAnswer()

    try:
        client_id = int(POST['id'])
        kind      = POST['kind']
        x         = int(POST['x'])
        y         = int(POST['y'])
        graph     = Graph.objects.get(pk=graph_id, deleted=False)
        assert(kind in notations.by_kind[graph.kind]['nodes'])

        command = commands.AddNode.create_of(graph_id, client_id, kind, x, y)
        command.do()

        response = HttpResponse(command.node.to_json(), 'application/javascript', status=201)
        response['Location'] = reverse('node', args=[graph.pk, command.node.pk])
        return response

    # a int conversion of one of the parameters failed or kind is not supported by the graph
    except ValueError, AssertionError:
        raise HttpResponseBadRequestAnswer()

    # the looked up graph does not exist
    except ObjectDoesNotExist:
        raise HttpResponseNotFoundAnswer()

    # should never happen, but for completeness enlisted here
    except MultipleObjectsReturned:
        raise HttpResponseServerErrorAnswer()

@login_required
@csrf_exempt
@transaction.commit_on_success
def node(request, graph_id, node_id):
    """
    Delete node from graph stored in the backend
    API Request:  DELETE /api/graphs/[graphID]/nodes/[nodeID], no body
    API Response: no body, status code 204

    Change property of a node
    API Request:            POST /api/graphs/[graphID]/nodes/[nodeID]
    API Request Parameters: key=... , value=...
    API Response:           no body, status code 204

    Change position of a node
    API Request:            POST /api/graphs/[graphID]/nodes/[nodeID]
    API Request Parameters: xcoord=... , ycoord=...
    API Response:           no body, status code 204

    Morph node to another type
    API Request:            POST /api/graphs/[graphID]/nodes/[nodeID]
    API Request Parameters: type=[NODE_TYPE]
    API Response:           no body, status code 204
    """
    if request.is_ajax():
        try:
            g=Graph.objects.get(pk=graph_id, deleted=False)
            n=Node.objects.get(graph=g, client_id=node_id, deleted=False)
        except:
            raise HttpResponseBadRequestAnswer()
        if request.method == 'DELETE':
            # delete node
            try:
                # remove edges explicitly to keep history
                for e in n.outgoing.all():
                    e.deleted=True
                    e.save()
                    c=History(command=Commands.DEL_EDGE, graph=g, edge=e)
                    c.save()
                for e in n.incoming.all():
                    e.deleted=True
                    e.save()
                    c=History(command=Commands.DEL_EDGE, graph=g, edge=e)
                    c.save()
                n.deleted=True
                n.save()
                c=History(command=Commands.DEL_NODE, graph=g, node=n)
                c.save()
            except:
                raise HttpResponseBadRequestAnswer()                        
            else:
                return HttpResponseNoResponse()
        elif request.method == 'POST':
            if 'xcoord' in request.POST and 'ycoord' in request.POST:
                try:
                    oldxcoord=n.xcoord
                    oldycoord=n.ycoord
                    n.xcoord = request.POST['xcoord']
                    n.ycoord = request.POST['ycoord']
                    n.save()
                    c=History(command=Commands.CHANGE_COORD, graph=g, node=n, oldxcoord=oldxcoord, oldycoord=oldycoord)
                    c.save()
                except:
                    raise HttpResponseBadRequestAnswer()
                return HttpResponseNoResponse()
            elif 'key' in request.POST and 'value' in request.POST:
                setNodeProperty(n, request.POST['key'], request.POST['value'])
                return HttpResponseNoResponse()
            elif 'type' in request.POST:
                #TODO change node type          
                return HttpResponseNoResponse()
            else:
                raise HttpResponseBadRequestAnswer()
        raise HttpResponseNotAllowedAnswer(['DELETE','POST'])

@login_required
@csrf_exempt
@transaction.commit_on_success
def edges(request, graph_id, node_id):
    """
    Add new edge to a node stored in the backend
    API Request:            POST /api/graphs/[graphID]/nodes/[nodeID]/edges
    API Request Parameters: destination=[nodeID]
    API Response:           no body, status code 201, location URI for new edge and its ID
    """
    if request.is_ajax():
        if request.method == 'POST':
            if 'destination' in request.POST:
                try:
                    client_id=int(request.POST['id'])
                    g=Graph.objects.get(pk=graph_id, deleted=False)
                    n=Node.objects.get(graph=g, client_id=node_id, deleted=False)
                    d=Node.objects.get(graph=g, client_id=request.POST['destination'], deleted=False)
                    e=Edge(client_id=client_id, src=n, dest=d)
                    e.save()
                    c=History(command=Commands.ADD_EDGE, graph=g, edge=e)
                    c.save()
                except Exception, e:
                    raise HttpResponseBadRequestAnswer()
                else:
                    responseBody = e.to_json()
                    response=HttpResponse(responseBody, status=201)
                    response['Location']=reverse('edge', args=[g.pk, n.pk, e.pk])
                    return response
        raise HttpResponseNotAllowedAnswer(['POST'])

@login_required
@transaction.commit_on_success
@csrf_exempt
def edge(request, graph_id, node_id, edge_id):
    """
    Delete the given edge that belongs to the given node
    API Request:  DELETE /api/graphs/[graphID]/nodes/[nodeID]/edges/[edgeID], no body
    API Response: no body, status code 204
    """
    if request.is_ajax():
        try:
            g=Graph.objects.get(pk=graph_id, deleted=False)
            n=Node.objects.get(graph=g, client_id=node_id, deleted=False)
            e=Edge.objects.get(client_id=edge_id, src=n, deleted=False)
        except:
            raise HttpResponseBadRequestAnswer()

        if request.method == 'DELETE':
            try:
                e.deleted=True
                e.save()
                c=History(command=Commands.DEL_EDGE, graph=g, edge=e)
                c.save()
            except:
                raise HttpResponseBadRequestAnswer()
            else:
                return HttpResponseNoResponse()

        raise HttpResponseNotAllowedAnswer(['DELETE'])
