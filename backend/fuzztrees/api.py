from django.http import HttpResponse, HttpResponseNotAllowed
from fuzztrees.models import Graph
import json

def undos(request):
	pass
	
def redos(request):
	pass
	
def graph(request, graph_id):
	if request.is_ajax():
		if request.method == 'GET':
			g=Graph.objects.get(pk=graph_id, owner=request.user)
			top=g.nodes.get(root=True)
			#fan={'id': 'fan', 'name': 'Fan'}
			#chip={'id': 'chip', 'name': 'Chip'}
			#cpu={'id': 'cpu', 'name': 'CPU', 'children': [fan, chip]}
			#disc={'id': 'disc', 'name': 'Disc'}
			#tree={'id': 'tree', 'name': 'TOP', 'children': [cpu, disc]}	
			data=json.dumps(top.getTreeDict())
			return HttpResponse(data, 'application/javascript')
		return HttpResponseNotAllowed(['GET']) 
	
def nodes(request):
	pass	
	
def node(request):
	pass
	
	