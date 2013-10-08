from django.db import models
from graph import Graph
from south.modelsinspector import add_introspection_rules

class NativeXmlField(models.Field):
    def db_type(self, connection):
        return 'xml'
add_introspection_rules([], ["^FuzzEd\.models\.job\.NativeXmlField"])        

class Job(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    CUTSETS_JOB   = 'CUTSETS'
    TOP_EVENT_JOB = 'TOPEVENT'
    EPS_RENDERING_JOB = 'EPS'
    PDF_RENDERING_JOB = 'PDF'    

    JOB_TYPES = (
        (CUTSETS_JOB,   'Cutset computation'),
        (TOP_EVENT_JOB, 'Top event calculation'),
        (EPS_RENDERING_JOB, 'EPS rendering job'),
        (PDF_RENDERING_JOB, 'PDF rendering job')
    )    

    graph = models.ForeignKey(Graph, null=False, related_name='jobs')
    name  = models.CharField(max_length=255, null=True)     # For internal names used by the backend
    kind  = models.CharField(max_length=127, choices=JOB_TYPES)
    done = models.BooleanField(default=False)               # Backend is done with this, can be deleted after delivery
    created = models.DateTimeField(auto_now_add=True, editable=False)
    data = NativeXmlField(null=True)                        # The graph as xml, input for the backend services
