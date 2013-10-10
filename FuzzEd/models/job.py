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

class Job(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    # These strings must be lowercase, since they travel through PostgreSQL notification,
    # which makes everything lower case
    CUTSETS_JOB   = 'cutsets'
    TOP_EVENT_JOB = 'topevent'
    EPS_RENDERING_JOB = 'eps'
    PDF_RENDERING_JOB = 'pdf'    
    LATEX_RENDERING_JOB = 'latex'
    PING_JOB = 'ping'    

    JOB_TYPES = (
        (CUTSETS_JOB,   'Cutset computation'),
        (TOP_EVENT_JOB, 'Top event calculation'),
        (EPS_RENDERING_JOB, 'EPS rendering job'),
        (PDF_RENDERING_JOB, 'PDF rendering job'),
        (LATEX_RENDERING_JOB, 'Latex rendering job'),
        (PING_JOB, 'Backend ping')
    )    

    graph = models.ForeignKey(Graph, null=True, related_name='jobs')
    secret  = models.CharField(max_length=64, default=str(uuid.uuid4()))     
    kind  = models.CharField(max_length=127, choices=JOB_TYPES)
    done = models.BooleanField(default=False)                               # Backend is done with this, can be deleted after delivery
    created = models.DateTimeField(auto_now_add=True, editable=False)
    result = models.FileField(upload_to='jobs', null=True)

    def input_data(self):
        ''' Used by the API to get the input data needed for the particular job type.'''
        if job.kind in (Job.CUTSETS_JOB, Job.TOP_EVENT_JOB):
            return job.graph.to_xml(), 'application/xml'
        elif job.kind in (Job.EPS_RENDERING_JOB, Job.PDF_RENDERING_JOB, LATEX_RENDERING_JOB):
            return job.graph.to_tikz(), 'application/text'
        assert(False)

@receiver(post_save, sender=Job)
def job_post_save(sender, instance, **kwargs):
    ''' Informs notification listeners using the PostgresSQL NOTIFY / LISTEN tools.
        Standard Postgres semantics apply, so if a listener does not pull a messages, than
        it is queued by the database.
        The payload contains the job files URL, which allows the listener to download
        and upload the input / output files for this job.
    '''
    #TODO: job_files_url = reverse('job_files', kwargs={'job_secret': instance.secret})
    job_files_url = settings.SERVER + '/api/jobs/'+instance.secret+'/files'
    cursor = connection.cursor()
    cursor.execute("NOTIFY %s, '%s';"%(instance.kind, job_files_url))
    transaction.commit_unless_managed()

