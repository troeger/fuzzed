import base64
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie import fields
from FuzzEd.models import Job
from django.conf.urls import url
from django.core.files.uploadedfile import SimpleUploadedFile

import logging,json
import common
from django.utils import http

logger = logging.getLogger('FuzzEd')

class JobResource(common.JobResource):
    """
        An API resource for jobs.
        It behaves differently than the job resource API for frontend and external clients,
        since it only focuses on feeding the backend daemon(s).
    """
    class Meta:
        queryset = Job.objects.all()
        detail_allowed_methods = ['get', 'patch']
        detail_uri_name = 'secret'

    graph = fields.ToOneField('FuzzEd.api.common.GraphResource', 'graph')

    def prepend_urls(self):
        """
            Make sure that job access is only possible with the job secret.
            This gives us the liberty to avoid any shared secret between backend and frontend,
            since it is part of each single job URL.
            Ultimatively, this means that backend daemon(s) do not need to authenticate at all.
        """
        return [
            url(r"^jobs/(?P<secret>[\w\d_.-]+)$",
                self.wrap_view('dispatch_detail'),
                name="job"),
        ]

    def get_detail(self, request, **kwargs):
        """
            Allows the backend to retrieve the job input file.
        """
        basic_bundle = self.build_bundle(request=request)
        try:
            job = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        logger.debug("Delivering data for job %d"%job.pk)
        response = HttpResponse()
        response.content, response['Content-Type'] = job.input_data()
        logger.debug(response.content)
        return response


    def patch_detail(self, request, **kwargs):
        """
            Allows the backend to upload the result file(s).
            We could also override obj_update, which is
            the Tastypie intended-way of having a custom PATCH implementation, but this
            method gets a full updated object bundle that is expected to be directly written
            to the object. In this method, we still have access to what actually really
            comes as part of the update payload.

            The result comes as 'application/json' dictionary content,
            with an entry for the exit code of the backend service and the base64-encoded file data.

            If the resource is updated, return ``HttpAccepted`` (202 Accepted).
            If the resource did not exist, return ``HttpNotFound`` (404 Not Found).
        """
        try:
            # Fetch relevant job object as Tastypie does it
            basic_bundle = self.build_bundle(request=request)
            job = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        if job.done():
            logger.error("Job already done, discarding uploaded results")
            return HttpResponse(status=202)     # This return code is a lie, but mitigates duplicate result submission
        else:
            logger.debug("Storing result data for job %d"%job.pk)
            try:
                result = json.loads(request.body)
                assert('exit_code' in result)
            except:
                return HttpBadRequest()
            job.exit_code = result['exit_code']   
            if "file_name" in result:
                # Retrieve binary file and store it
                job.result = base64.b64decode(result['file_data'])
                if not job.requires_download:
                    logger.debug(''.join(job.result))
	    job.save()
        return HttpResponse(status=202)
