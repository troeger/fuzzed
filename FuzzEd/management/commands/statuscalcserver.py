from django.core.management.base import BaseCommand, CommandError
from analysis import calcserver

class Command(BaseCommand):
	help = 'Prints the list of jobs running in the calc serber'

	def handle(self, *args, **options):
		print "Job\tStatus"
		print "---\t------"
		for k,v in calcserver.listJobs().iteritems():
			print "%s\t%s"%(k,v)