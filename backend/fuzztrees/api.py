from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from fuzztrees.models import *
from nodes_config import NODE_TYPES, NODE_TYPE_IDS
import json
import traceback

@login_required
@csrf_exempt
def undos(request, graph_id):
	"""
	Fetch undo command stack from backend
	API Request:  GET /api/graphs/[graphID]/undos, no body
	API Response: JSON body with command array of undo stack

	Tell the backend that an undo has been issued in the model
	API Request:  POST /api/graphs/[graphID]/undos, no body
	API Response: no body, status code 204
	"""
	if request.is_ajax():
		if request.method == 'GET':
			#TODO: Fetch undo stack for the graph
			return HttpResponse(status=200)
		elif request.method == 'POST':
			#TODO: Perform top command on undo stack
			return HttpResponse(status=204)
		return HttpResponseNotAllowed(['GET', 'POST']) 

@login_required
@csrf_exempt
def redos(request, graph_id):
	"""
	Fetch redo command stack from backend
	API Request:  GET /api/graphs/[graphID]/redos, no body
	API Response: JSON body with command array of redo stack

	Tell the backend that an redo has been issued in the model
	API Request:  POST /api/graphs/[graphID]/redos, no body
	API Response: no body, status code 204
	"""
	if request.is_ajax():
		if request.method == 'GET':
			#TODO Fetch redo stack for the graph
			return HttpResponse(status=200)
		elif request.method == 'POST':
			#TODO Perform top command on redo stack
			return HttpResponse(status=204)
		return HttpResponseNotAllowed(['GET', 'POST']) 

@login_required
@transaction.commit_on_success
@csrf_exempt
def graphs(request):
	"""
	Add new graph in the backend
	API Request:            POST /api/graphs
	API Request Parameters: type=[GRAPH_TYPE], name=[graph name]
	API Response:           no body, status code 201, location URI for new graph and its ID
	"""	
	if request.is_ajax():
		if request.method == 'POST':
			if 'type' in request.POST and 'name' in request.POST:
				# add new graph		
				try:
					t=int(request.POST['type'])
					if t==GraphTypes.FUZZ_TREE:
						createFuzzTreeGraph(request.user, request.POST['name'])
					else:
						return HttpResponseBadRequest()	
				except:
					return HttpResponseBadRequest()	
				else:		
					response=HttpResponse(status=201)
					response['Location']=reverse('graph', args=[g.pk])
					response['ID'] = g.pk
					return response
			else:
				return HttpResponseBadRequest()
		return HttpResponseNotAllowed(['POST']) 

@login_required
def graph(request, graph_id):
	"""
	Fetch serialized current graph from backend
	API Request:  GET /api/graphs/[graphID] , no body
	API Response: JSON body with serialized graph
	"""
	if request.is_ajax():
		if request.method == 'GET':
			# fetch graph 
			try:
				g=Graph.objects.get(pk=graph_id, owner=request.user, deleted=False)
			except:
				return HttpResponseNotFound()
			data=json.dumps(g.toJsonDict())
			return HttpResponse(data, 'application/javascript')
		return HttpResponseNotAllowed(['GET']) 
	
@login_required
@transaction.commit_on_success
@csrf_exempt
def nodes(request, graph_id):
	"""
	Add new node to graph stored in the backend
	API Request:            POST /api/graphs/[graphID]/nodes
	API Request Parameters: type=[NODE_TYPE], xcoord, ycoord
	API Response:           JSON object containing the node's ID, status code 201, location URI for new node
	"""

	if request.is_ajax():
		if request.method == 'POST':
			if 'type' in request.POST and 'xcoord' in request.POST and 'ycoord' in request.POST:
				try:
					client_id=int(request.POST['id'])
					t=NODE_TYPE_IDS[request.POST['type']]
					assert(t in NODE_TYPES)
					g=Graph.objects.get(pk=graph_id, deleted=False)
					n=Node(client_id=client_id, type=t, graph=g, xcoord=request.POST['xcoord'], ycoord=request.POST['ycoord'])
					n.save()
					c=History(command=Commands.ADD_NODE, graph=g, node=n)
					c.save()
				except:
					return HttpResponseBadRequest()
				else:
					responseBody = json.dumps(n.toJsonDict())
					response=HttpResponse(responseBody, 'application/javascript', status=201)
					response['Location']=reverse('node', args=[g.pk, n.pk])
					return response
		return HttpResponseNotAllowed(['POST']) 

@login_required
@transaction.commit_on_success
@csrf_exempt
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
			n=Node.objects.get(client_id=node_id, deleted=False)
		except:
			return HttpResponseBadRequest()
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
				return HttpResponseBadRequest()						
			else:
				return HttpResponse(status=204)
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
					return HttpResponseBadRequest()
				return HttpResponse(status=204)
			elif 'key' in request.POST and 'value' in request.POST:
				print n, request.POST
				setNodeProperty(n, request.POST['key'], request.POST['value'])
				return HttpResponse(status=204)
			elif 'type' in request.POST:
				#TODO change node type			
				return HttpResponse(status=204)
			else:
				return HttpResponseBadRequest()
		return HttpResponseNotAllowed(['DELETE','POST'])

@login_required
@transaction.commit_on_success
@csrf_exempt
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
					n=Node.objects.get(client_id=node_id, deleted=False)
					d=Node.objects.get(client_id=request.POST['destination'], deleted=False)
					e=Edge(client_id=client_id, src=n, dest=d)
					e.save()
					c=History(command=Commands.ADD_EDGE, graph=g, edge=e)
					c.save()
				except Exception, e:
					return HttpResponseBadRequest()
				else:
					responseBody = json.dumps(e.toJsonDict())
					response=HttpResponse(responseBody, status=201)
					response['Location']=reverse('edge', args=[g.pk, n.pk, e.pk])
					return response
		return HttpResponseNotAllowed(['POST'])

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
			n=Node.objects.get(client_id=node_id, deleted=False)
			e=Edge.objects.get(client_id=edge_id, src=n, deleted=False)
		except:
			return HttpResponseBadRequest()

		if request.method == 'DELETE':
			try:
				e.deleted=True
				e.save()
				c=History(command=Commands.DEL_EDGE, graph=g, edge=e)
				c.save()
			except:
				return HttpResponseBadRequest()
			else:
				return HttpResponse(status=204)

		return HttpResponseNotAllowed(['DELETE'])
