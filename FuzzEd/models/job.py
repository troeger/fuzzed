from django.db import models, connection, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from graph import Graph
from south.modelsinspector import add_introspection_rules
from FuzzEd import settings
import uuid

class NativeXmlField(models.Field):
    def db_type(self, connection):
        return 'xml'
add_introspection_rules([], ["^FuzzEd\.models\.job\.NativeXmlField"])        

def gen_uuid():
    return str(uuid.uuid4())

class Job(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    # These strings must be lowercase, since they travel through PostgreSQL notification,
    # which makes everything lower case
    CUTSETS_JOB   = 'cutsets'
    TOP_EVENT_JOB = 'topevent'
    EPS_RENDERING_JOB = 'eps'
    PDF_RENDERING_JOB = 'pdf'    

    JOB_TYPES = (
        (CUTSETS_JOB,   'Cutset computation'),
        (TOP_EVENT_JOB, 'Top event calculation'),
        (EPS_RENDERING_JOB, 'EPS rendering job'),
        (PDF_RENDERING_JOB, 'PDF rendering job')
    )

    # List of job types that generate files that require a download.
    # This means their result will not be served directly but rather a URL to it.
    DOWNLOAD_TYPES = frozenset({EPS_RENDERING_JOB, PDF_RENDERING_JOB})

    graph = models.ForeignKey(Graph, null=True, related_name='jobs')
    graph_modified = models.DateTimeField()                                # Detect graph changes during job execution
    secret  = models.CharField(max_length=64, default=gen_uuid)            # Unique secret for this job
    kind  = models.CharField(max_length=127, choices=JOB_TYPES)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    result = models.FileField(upload_to='jobs', null=True)                 # Result file for this job
    exit_code = models.IntegerField(null=True)                             # Exit code for this job, NULL if pending

    def input_data(self):
        ''' Used by the API to get the input data needed for the particular job type.'''
        if self.kind in (Job.CUTSETS_JOB, Job.TOP_EVENT_JOB):
            return self.graph.to_xml(), 'application/xml'
        elif self.kind in (Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB):
            return self.graph.to_tikz(), 'application/text'
        assert(False)

    def done(self):
        return self.exit_code is not None

    def requires_download(self):
        return self.kind in Job.DOWNLOAD_TYPES

@receiver(post_save, sender=Job)
def job_post_save(sender, instance, created, **kwargs):
    ''' Informs notification listeners using the PostgresSQL NOTIFY / LISTEN tools.
        Standard Postgres semantics apply, so if a listener does not pull a messages, than
        it is queued by the database.
        The payload contains the job URL prefix with a secret, which allows the listener to 
        perform according actions
    '''
    if created:
        # The only way to determine our own hostname + port number at runtime in Django
        # is from an HttpRequest object, which we do not have here. 
        # Option 1 is to fetch this information from the HttpRequest and somehow move it here.
        # This works nice as long as LiveServerTestCase is not used, since the Django Test
        # Client still accesses the http://testserver URL and not the live server URL.
        # We therefore take the static approach with a setting here, which is overriden
        # by the test suite run accordingly

        #TODO: job_files_url = reverse('job_files', kwargs={'job_secret': instance.secret})
        job_files_url = settings.SERVER + '/api/jobs/'+instance.secret+'/'
        cursor = connection.cursor()
        cursor.execute("NOTIFY %s, '%s';"%(instance.kind, job_files_url))
        #print "Notification to: "+str(cursor.db.connection.dsn)
        transaction.commit_unless_managed()

