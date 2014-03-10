"""
    This is the API for everybody else beside the frontend. Access restrictions here are managed by OAuth.

    Security: No resource ownership checks ('is this his graph ?') should happen here, 
              only access security ('is he allowed to use that functionality ?').
"""

from FuzzEd.middleware import HttpResponseServerErrorAnswer
from oauth2_provider.views.generic import ProtectedResourceView

import time
import api

class GraphPdf(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        assert('graph_id' in kwargs)
        print request.user
        graph_id = int(kwargs['graph_id'])
        job = api.job_create(request.user, graph_id, 'pdf')
        while not job.done():
            # TODO: Move this to central settings.ini
            time.sleep(2)
        status, job = api.job_status(request.user, job.pk)
        if status == 0:
            return api.graph_download(request.user, graph_id, 'pdf')
        else:
            raise HttpResponseServerErrorAnswer("Internal error, could not create PDF file. Try the web frontend.")

#@protected_resource
#def graph_download_graphml(request, graph_id):  
#    return api.graph_download(request.user, graph_id, 'graphml')

#@protected_resource
#def graph_download_tex(request, graph_id):  
#    return api.graph_download(request.user, graph_id, 'tex')

