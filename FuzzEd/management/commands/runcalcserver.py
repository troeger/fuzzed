from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
	help = 'Starts the analysis engine remotely used by the FuzzEd backend'

	def handle(self, *args, **options):
		os.system('java -jar analysis/jar/fuzzTreeAnalysis.jar -runServer')
