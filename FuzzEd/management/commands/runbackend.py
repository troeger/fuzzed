from django.core.management.base import BaseCommand, CommandError
from analysis import top_event_probability
from subprocess import Popen, PIPE
import os, sys, beanstalkc

def printAnalysisServerStatus():
	print 'Job\tStatus'
	print '---\t------'

	for job_id, status in top_event_probability.list_jobs().iteritems():
		print '%s\t%s' % (job_id, status)	

def printBeanstalkStatus():
	b = beanstalkc.Connection(parse_yaml=False)
	print b.stats()

class Command(BaseCommand):
	help = 'Starts the backend services'

	def handle(self, *args, **options):
		print "Starting beanstalkd messaging server ..."
		beanstalk = Popen(["beanstalkd"], stdout=PIPE, stderr=PIPE)
		if beanstalk.returncode != None:
			print "Error %u while starting beanstalkd"%beanstalk.returncode
			exit(-1)
		print "Starting Java analysis server ..."
		analysis = Popen(["java","-jar","analysis/jar/fuzzTreeAnalysis.jar","-runServer"], stderr=PIPE, stdout=PIPE)
		if analysis.returncode != None:
			print "Error %u while starting Java analysis server"%analysis.returncode
			beanstalk.terminate()
			exit(-1)
		while 1:
			print "Press any key for status information, or 'q' for quitting ..."
			line = sys.stdin.readline()
			if line.startswith('q'):
				analysis.terminate()
				beanstalk.terminate()
				exit(0)
			else:
				print 79*"="
				print "Beanstalkd stats"
				print 79*"="
				printBeanstalkStatus()
				print 79*"="
				print "Java analysis server stats"
				print 79*"="
				printAnalysisServerStatus()
				print 79*"="


