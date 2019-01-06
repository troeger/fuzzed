from django.core.management.base import BaseCommand
import FuzzEd

class Command(BaseCommand):
    help = 'Prints the FuzzEd version and exits.'

    def handle(self, *args, **options):
    	print FuzzEd.VERSION
