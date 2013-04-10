from django.db import models
from graph import Graph

class Job(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    CUTSETS_JOB   = 'C'
    TOP_EVENT_JOB = 'T'

    JOB_TYPES = (
        (CUTSETS_JOB,   'Cutset computation'),
        (TOP_EVENT_JOB, 'Top event calculation')
    )    

    graph = models.ForeignKey(Graph, null=False, related_name='jobs')
    name  = models.CharField(max_length=255)
    kind  = models.CharField(max_length=127, choices=JOB_TYPES)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    configurations = models.IntegerField(default=0)
    nodes = models.IntegerField(default=0)
    