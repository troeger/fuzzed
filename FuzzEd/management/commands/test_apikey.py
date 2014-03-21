from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    args = "<API key>"
    help = 'Test implementation of an app client, based on the API key.'

    def handle(self, *args, **options):
        server = "http://192.168.33.10:8000"
        r = requests.get(server+'/api/v1/graph/1/?format=tex', headers={'Authorization':'ApiKey admin:'+args[0]})
        print r.request.headers
        if r.status_code != 200:
            print("Error: <%u>"%r.status_code)
        else:
            print r.text






