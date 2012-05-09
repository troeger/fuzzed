from django.http import HttpResponse
import json as simplejson

def json(request):
	if request.is_ajax():
		if request.method == 'POST':
			print 'Got POST request with JSON data'
			print request.POST
		elif request.method == 'GET':
			fan={'id': 'fan', 'name': 'Fan'}
			chip={'id': 'chip', 'name': 'Chip'}
			cpu={'id': 'cpu', 'name': 'CPU', 'children': [fan, chip]}
			disc={'id': 'disc', 'name': 'Disc'}
			tree={'id': 'tree', 'name': 'TOP', 'children': [cpu, disc]}	
			return HttpResponse(simplejson.dumps(tree), 'application/javascript')
	return HttpResponse(status=200) 
