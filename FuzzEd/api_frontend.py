"""
	This is the API for the web frontend. Access restrictions are managed by Django session handling.

    Only frontend-specific functionality should be implemented in here, mainly everything that revolves
    around URL handling. Basic functionality (e.g. fiddling around with model instances) is supposed
    to live in api.py.

	Security: No resource ownership checks ('is this his graph ?') should happen here, 
	          only access security ('is he allowed to use that functionality ?').
"""

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.core.urlresolvers import reverse
from FuzzEd.middleware import HttpResponse, HttpResponseAccepted

import api

@login_required
@csrf_exempt
@require_GET
def graph_download(request, graph_id):
	'''
        Provides a download response of the graph in the given format in the GET parameter, 
        or an HTTP error if the rendering job for the export format is not ready so far.
    '''
	export_format = request.GET.get('format', 'xml')
	return api.graph_download(request.user, graph_id, export_format)

@login_required
@csrf_exempt
@require_GET
def job_status(request, job_id):
    ''' Returns the status information for the given job.
        202 is delivered if the job is pending, otherwise the result is immediately returned.
        The result may be the actual text data, or a download link to a binary file.
    '''
    status, job = api.job_status(request.user, job_id)

    if status == 0:		# done, valid result
        if job.requires_download():
            # Return the URL to the file created by the job
            return HttpResponse(reverse('frontend_graph_download', args=[job.graph.pk]))
        else:
            # Serve directly
            return HttpResponse(job.result_rendering())
    elif status == 1:   # done and error
        raise HttpResponseServerErrorAnswer("We have an internal problem analyzing this graph. Sorry! The developers are informed.")
    elif status == 2:   # Pending             
        return HttpResponseAccepted()
    elif status == 3:   # Does not exists
        raise HttpResponseNotFoundAnswer()

@login_required
@csrf_exempt
@require_GET
def job_create(request, graph_id, job_kind):
    '''
	    Starts a job of the given kind for the given graph.
    	It is intended to return immediately with job information for the frontend.
    '''
    job = api.job_create(request.user, graph_id, job_kind)
    response = HttpResponse(status=201)
    response['Location'] = reverse('frontend_job_status', args=[job.pk])
    return response


