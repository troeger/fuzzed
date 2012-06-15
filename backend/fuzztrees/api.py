from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from fuzztrees.models import Graph, Node, Edge, History, GRAPH_JS_TYPE, Commands
from nodes_config import NODE_TYPES
import json

@login_required
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
@transaction.commit_manually
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
					assert(t in GRAPH_JS_TYPE)
					g=Graph(name=request.POST['name'], owner=request.user, type=t)
					g.save()
					c=History(command=Commands.ADD_GRAPH, graph=g)
					c.save()
					transaction.commit()
				except:
					transaction.rollback()
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
			top=g.nodes.get(root=True)
			#fan={'id': 'fan', 'name': 'Fan'}
			#chip={'id': 'chip', 'name': 'Chip'}
			#cpu={'id': 'cpu', 'name': 'CPU', 'children': [fan, chip]}
			#disc={'id': 'disc', 'name': 'Disc'}
			#tree={'id': 'tree', 'name': 'TOP', 'children': [cpu, disc]}	
			data=json.dumps(top.getTreeDict())
			return HttpResponse(data, 'application/javascript')
		return HttpResponseNotAllowed(['GET']) 
	
@login_required
@transaction.commit_manually
def nodes(request, graph_id):
	"""
	Add new node to graph stored in the backend
	API Request:            POST /api/graphs/[graphID]/nodes
	API Request Parameters: parent=[parentID], type=[NODE_TYPE], xcoord, ycoord
	API Response:           no body, status code 201, location URI for new node and its ID
	"""
	if request.is_ajax():
		if request.method == 'POST':
			if 'parent' in request.POST and 'type' in request.POST and 'xcoord' in request.POST and 'ycoord' in request.POST:
				try:
					t=int(request.POST['type'])
					assert(t in NODE_TYPES)
					g=Graph.objects.get(pk=graph_id, deleted=False)
					p=Node.objects.get(pk=request.POST['parent'], deleted=False)
					n=Node(type=t, graph=g, xcoord=request.POST['xcoord'], ycoord=request.POST['ycoord'] )
					n.save()
					c=History(command=Commands.ADD_NODE, graph=g, node=n)
					c.save()
					e=Edge(src=p, dest=n)
					e.save()
					c2=History(command=Commands.ADD_EDGE, graph=g, edge=e)
					c2.save()
					transaction.commit()
				except Exception, e:
					transaction.rollback()
					return HttpResponseBadRequest()			
				else:					
					response=HttpResponse(status=201)
					response['Location']=reverse('node', args=[g.pk, n.pk])
					response['ID'] = n.pk
					return response
		return HttpResponseNotAllowed(['POST']) 

@login_required	
def node(request, graph_id, node_id):
	"""
	Delete node from graph stored in the backend
	API Request:  DELETE /api/graphs/[graphID]/nodes/[nodeID], no body
	API Response: no body, status code 204

	Link node to another parent in the graph	
	API Request:            POST /api/graphs/[graphID]/nodes/[nodeID] 
	API Request Parameters: parent=[nodeID],  xcoord=..., ycoord=...
	API Response:           no body, status code 204

	Change property of a node
	API Request:            POST /api/graphs/[graphID]/nodes/[nodeID]
	API Request Parameters: key=... , val=...
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
			n=Node.objects.get(pk=node_id, deleted=False)
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
				transaction.commit()
			except:
				transaction.rollback()
				return HttpResponseBadRequest()						
			else:
				return HttpResponse(status=204)
		elif request.method == 'POST':
			if 'parent' in request.POST and 'xcoord' in request.POST and 'ycoord' in request.POST:
				# relink node
				try:
					# - Change node position
					c=History(command=Commands.CHANGE_COORD, graph=g, oldxcoord=n.xcoord, oldycoord=n.ycoord)
					c.save()
					n.xcoord=request.POST['xcoord']
					n.ycoord=request.POST['ycoord']					
					n.save()
					# - get new parent node and remove edge from old parent to this node
					p=Node.objects.get(pk=request.POST['parent'], deleted=False)				
					# -> this will throw an exception if the node has more than one incoming edge
					# -> this is good, since it would mean that we have more than one parent,
					# -> which is not modelled in the current API
					e=Edge.objects.get(dest=n, deleted=False)
					e.deleted=True
					e.save()
					c=History(command=Commands.DEL_EDGE, graph=g, edge=e)
					c.save()
					# - link new parent with this node
					new_e=Edge(src=p, dest=n)
					new_e.save()
					c=History(command=Commands.ADD_EDGE, graph=g, edge=new_e)
					c.save()
					transaction.commit()
				except:
					transaction.rollback()
					return HttpResponseBadRequest()						
				else:
					return HttpResponse(status=204)
			elif 'xcoord' in request.POST and 'ycoord' in request.POST:
				#TODO reposition node
				return HttpResponse(status=204)
			elif 'key' in request.POST and 'val' in request.POST:
				#TODO change node property
				return HttpResponse(status=204)
			elif 'type' in request.POST:
				#TODO change node type			
				return HttpResponse(status=204)
			else:
				return HttpResponseBadRequest()
		return HttpResponseNotAllowed(['DELETE','POST']) 
	
	