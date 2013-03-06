from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	help = 'Starts the analysis engine remotely used by the FuzzEd backend'

	def handle(self, *args, **options):
