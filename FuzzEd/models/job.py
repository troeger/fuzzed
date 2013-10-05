from django.db import models
from graph import Graph

class Job(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    CUTSETS_JOB   = 'C'
    TOP_EVENT_JOB = 'T'
    EPS_RENDERING_JOB = 'E'
    PDF_RENDERING_JOB = 'P'    
    STATE_NEW = 'N'
    STATE_FETCHED = 'F'
    STATE_DONE = 'D'

    JOB_TYPES = (
        (CUTSETS_JOB,   'Cutset computation'),
        (TOP_EVENT_JOB, 'Top event calculation'),
        (EPS_RENDERING_JOB, 'EPS rendering job'),
        (PDF_RENDERING_JOB, 'PDF rendering job')
    )    

    STATE_TYPES = (
        (STATE_NEW, 'Job was not fetched so far.'),
        (STATE_FETCHED, 'Job was fetched.'),
        (STATE_DONE, 'Result is available.'))

    graph = models.ForeignKey(Graph, null=False, related_name='jobs')
    name  = models.CharField(max_length=255, null=True)
    kind  = models.CharField(max_length=127, choices=JOB_TYPES)
    state = models.CharField(max_length=127, choices=STATE_TYPES, default=STATE_NEW)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    result = models.FileField('jobs')    
