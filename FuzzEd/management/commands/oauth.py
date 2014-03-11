from django.core.management.base import BaseCommand

# Make client OAuth library work without SSL, since the dev server is not available over SSL.
# This means transporting the client_secret readable, which would obviousely be a very stupid idea in production code.
import os
os.environ['DEBUG'] = '1'

import oauthlib
from requests_oauthlib import OAuth2Session

class Command(BaseCommand):
    # Make sure that client_id and client_secret are registered for 'client-credentials' auth type  
    args = "'<client_id>' '<client_secret>' [server]"
    help = 'Test implementation of an OAuth client against the dev server.'

    def handle(self, *args, **options):
        server = "http://192.168.33.10:8000"
        apps_url = "/o/applications/"   
        auth_base_url = "/o/authorize/"
        token_url = "/o/token/"
        if len(args) < 2:
            print "Register your application to get client_id and client_secret: "+server+apps_url
            exit(-1)
        elif len(args) > 2:
            server = args[2]

        client_id = args[0]
        client_secret = args[1]
        # Here starts the action
        client = oauthlib.oauth2.BackendApplicationClient(client_id)
        session = OAuth2Session(client_id, client=client)
        token = session.fetch_token(server+token_url, client_id=client_id, client_secret=client_secret)
        # Version 1 of using the gathered token, implicitely
        response = session.get(server+'/api/v1/graph/1/?format=tex')
        print response.content
        # Version 2, save the token somewhere and reuse it
        #session2 = OAuth2Session(client_id, token=token)
        #print session.get(server+'/api/graphs/1/tex')






