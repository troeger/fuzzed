from django.core.management.base import BaseCommand
import ore


class Command(BaseCommand):
    help = 'Prints the ORE version and exits.'

    def handle(self, *args, **options):
        print ore.VERSION
