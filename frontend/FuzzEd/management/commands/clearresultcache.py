from django.core.management.base import BaseCommand
from FuzzEd.models import Job, Result


class Command(BaseCommand):
    help = 'Clear all finished jobs with cached results'

    def handle(self, *args, **options):
        finished_jobs = Job.objects.filter(exit_code=0)
        print "%u finished jobs are stored ..."%len(finished_jobs)

        for j in finished_jobs:
                print "Deleting cached results for job %u"+j.pk
                results = Result.objects.filter(job=j)
                results.delete()

        print "Deleting finished jobs ..."
        finished_jobs.delete()
