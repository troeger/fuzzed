import os
from configurations.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ore.settings')
application = get_wsgi_application()
