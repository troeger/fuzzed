#from oauth2_provider.views.generic import ProtectedResourceView        see urls.py for further explanation

import logging
from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import ApiKey

logger = logging.getLogger('FuzzEd')

import common

class OurApiKeyAuthentication(ApiKeyAuthentication):
    """
        Our own authenticator version does not demand the user name to be part of the auth header.
    """

    def extract_credentials(self, request):
        if request.META.get('HTTP_AUTHORIZATION') and request.META['HTTP_AUTHORIZATION'].lower().startswith('apikey '):
            (auth_type, api_key) = request.META['HTTP_AUTHORIZATION'].split(' ')

            if auth_type.lower() != 'apikey':
                logger.debug("Incorrect authorization header: " + str(request.META['HTTP_AUTHORIZATION']))
                raise ValueError("Incorrect authorization header.")
            try:
                key = ApiKey.objects.get(key=api_key.strip())
            except:
                logger.debug("Incorrect API key in header: " + str(request.META['HTTP_AUTHORIZATION']))
                raise ValueError("Incorrect API key.")
            return key.user.username, api_key
        else:
            logger.debug("Missing authorization header: " + str(request.META))
            raise ValueError("Missing authorization header.")

class GraphResource(common.GraphResource):
    class Meta(common.GraphResource.Meta):
        authentication = OurApiKeyAuthentication()

class ProjectResource(common.ProjectResource):
    class Meta(common.ProjectResource.Meta):
        authentication = OurApiKeyAuthentication()
