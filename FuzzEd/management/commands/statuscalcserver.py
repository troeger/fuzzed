from django.core.management.base import BaseCommand
from analysis import top_event_probability

class Command(BaseCommand):
	help = 'Prints the list of jobs running on the analysis server'

	def handle(self, *args, **options):
		print 'Job\tStatus'
		print '---\t------'

		for job_id, status in top_event_probability.list_jobs().iteritems():
			print '%s\t%s' % (job_id, status)