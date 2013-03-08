from django.db import models
from graph import Graph

class Job(models.Model):
    class Meta:
        app_label = 'FuzzEd'

    CUTSETS_JOB = 'C'                       
    TOPEVENT_JOB = 'T' 

    JOBTYPES = (
        (CUTSETS_JOB, 'Cutset computation'),    
        (TOPEVENT_JOB, 'Top event calculation')
    )    

    graph = models.ForeignKey(Graph, null=False, related_name='jobs')
    name  = models.CharField(max_length=255)
    kind  = models.CharField(max_length=127, choices=JOBTYPES)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    configurations = models.IntegerField(default=0);
    nodes = models.IntegerField(default=0)
    