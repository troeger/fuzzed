"""
    This is the central internal FuzzEd API, used by different API's in the layers above.

    For these functions, access security is assumed to be given, 
    since this should be handled by higher API layers.
"""

from django.shortcuts import get_object_or_404
from FuzzEd.models import Graph, Job
from FuzzEd.middleware import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('FuzzEd')

def graph_download(user, graph_id, export_format):
    """
    Function: graph_download
        Provides a download response of the graph in the given format, or an HTTP error if 
        the rendering job for the export format is not ready so far.

        It is sufficient to prepare the HTTP response already here, since the link is independent
        from the the kind of API being used for access

    Parameters:
     user          - The requesting user's object in the model
     graph_id      - the id of the graph to be downloaded
     export_format - The demanded export format

    Returns:
     {HTTPResponse} a django response object
    """
    if user.is_staff:
        graph = get_object_or_404(Graph, pk=graph_id)
    else:
        graph = get_object_or_404(Graph, pk=graph_id, owner=user, deleted=False)        

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=%s.%s' % (graph.name, export_format)

    if export_format == 'xml':
        response.content = graph.to_xml()
        response['Content-Type'] = 'application/xml'
    elif export_format == 'graphml':
        response.content = graph.to_graphml()
        response['Content=Type'] = 'application/xml'
    elif export_format == 'json':
        response.content = graph.to_json()
        response['Content-Type'] = 'application/javascript'
    elif export_format == 'tex':
        response.content = graph.to_tikz()
        response['Content-Type'] = 'application/text'
    elif export_format in ('pdf', 'eps'):
        try:
            # Take the latest file that was successfully created
            # This is based on the assumption that nobody calls this function before the job is done
            job = graph.jobs.filter(kind=export_format).latest('created')
            if not job.done():
                raise HttpResponseNotFoundAnswer()
            response.content = job.result
            response['Content-Type'] = 'application/pdf' if export_format == 'pdf' else 'application/postscript'
        except ObjectDoesNotExist:
            raise HttpResponseNotFoundAnswer()
    else:
        raise HttpResponseNotFoundAnswer()
    return response


def job_create(user, graph_id, job_kind):
    """
        Starts a job of the given kind for the given graph.
        It is intended to return immediately with job object.
    """
    print user
    if user.is_staff:
        graph = get_object_or_404(Graph, pk=graph_id)
    else:
        graph = get_object_or_404(Graph, pk=graph_id, owner=user, deleted=False)

    job = Job(graph=graph, kind=job_kind, graph_modified=graph.modified)
    job.save()

    # return URL for job status information
    logger.debug('Created new %s job with ID %d for graph %d' % (job.kind, job.pk, graph.pk))
    return job
 
def job_status(user, job_id):
    ''' Returns the status information for the given job, and the job object if available.
        This API helper wraps functionality that is common to all frontend API versions of
        this call.
        0 - Job is done, deliver the result.
        1 - Job is done, but you can't deliver the result due to an error.
        2 - Job is not done, try again later.
        3 - Job does not exist, go away.
    '''
    try:
        job = Job.objects.get(pk=job_id)
        # Prevent cross-checking of jobs by different users
        assert(job.graph.owner == user or user.is_staff)
    except:
        # The job does not exist, or it shouldn't exist for this user.        
        return 3, None

    if job.done():
        if job.exit_code == 0:
            logger.debug("Job is done.")
            return 0, job
        else:
            logger.debug("Job is done, but with non-zero exit code.")
            mail_managers('Analysis of job %s ended with non-zero exit code.'%job.pk, job.graph.to_xml() )
            return 1, job
    else:       
        logger.debug("Job is pending.")
        return 2, job

