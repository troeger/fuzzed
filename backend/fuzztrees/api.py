from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from fuzztrees.models import Graph
import json

def undos(request, graph_id):
	if request.is_ajax():
		if request.method == 'GET':
			# Fetch undo stack for the graph
			return HttpResponse(status=200)
		elif request.method == 'POST':
			# Perform top command on undo stack
			return HttpResponse(status=200)
		return HttpResponseNotAllowed(['GET', 'POST']) 
	
def redos(request, graph_id):
	if request.is_ajax():
		if request.method == 'GET':
			# Fetch redo stack for the graph
			return HttpResponse(status=200)
		elif request.method == 'POST':
			# Perform top command on redo stack
			return HttpResponse(status=200)
		return HttpResponseNotAllowed(['GET', 'POST']) 
		
def graph(request, graph_id):
	if request.is_ajax():
		if request.method == 'GET':
			# fetch graph 
			try:
				g=Graph.objects.get(pk=graph_id, owner=request.user)
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
	
	
def nodes(request, graph_id):
	if request.is_ajax():
		if request.method == 'POST':
			if 'parent' in request.POST and 'type' in request.POST:
				# create node
				return HttpResponse(status=200)
		return HttpResponseNotAllowed(['POST']) 
	
def node(request, graph_id, node_id):
	if request.is_ajax():
		if request.method == 'DELETE':
			# delete node
			return HttpResponse(status=200)
		elif request.method == 'PUT':
			if 'parent' in request.POST:
				# relocate node
				return HttpResponse(status=200)
			elif 'key' in request.POST and 'val' in request.POST:
				# change node property
				return HttpResponse(status=200)
			elif 'type' in request.POST:
				# change node type			
				return HttpResponse(status=200)
			else:
				return HttpResponseBadRequest()
		return HttpResponseNotAllowed(['DELETE','PUT']) 
	
	