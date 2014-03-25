from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from graph import Graph
from FuzzEd.lib.jsonfield import JSONField

import json

class Result(models.Model):
    """
      Class: Project
      
      Fields:
       {Configuration}   configuration  -
       {Graph}           graph          -
       {str}             kind           -
       {JSON}            value          -
       {int}             value_sort     - 
       {JSON}            node_issues    -
                             
    """
  
    class Meta:
        app_label = 'FuzzEd'

    ANALYSIS_RESULT   = 'T'
    SIMULATION_RESULT = 'S'
    PDF_RESULT        = 'P'
    EPS_RESULT        = 'E'
    GRAPH_ISSUES      = 'G'
    RESULT_TYPES = [ (GRAPH_ISSUES, 'graphissues'), 
                     (SIMULATION_RESULT, 'simulation'), 
                     (ANALYSIS_RESULT, 'topevent'),
                     (PDF_RESULT, 'pdf'),
                     (EPS_RESULT, 'eps')]
    
    graph         = models.ForeignKey(Graph, related_name='results')
    job           = models.ForeignKey('Job', related_name='results')
    configuration = models.ForeignKey('Configuration', related_name='results', null=True, blank=True)
    kind          = models.CharField(max_length=1, choices= RESULT_TYPES)
    value         = JSONField(blank=True, null=True)
    value_sort    = models.IntegerField(blank=True, null=True) 
    binary_value  = models.BinaryField(blank=True, null=True)
    issues        = JSONField(blank=True, null=True)

    def is_binary(self):
        ''' Indicates if the result should be delivered directly to the frontend
            as file, or if it must be preprocessed with self.to_json().'''
        return self.kind in [Result.PDF_RESULT, Result.EPS_RESULT]

    def to_url(self):
        ''' Returns a binary result as view URL.'''
        assert(self.is_binary())
        if self.kind == Result.PDF_RESULT:
            kind = 'pdf'
        elif self.kind == Result.EPS_RESULT:
            kind = 'eps'
        return reverse('frontend_graph_download', args=[self.graph.pk]) + "?format="+kind

    def to_json(self):
        ''' Returns a non-binary result as frontend-compliant JSON.'''

        assert(not self.is_binary())

        json_result = {}
        json_result['columns'] = [  { 'mData': 'id',     'sTitle': 'Config' },
                                    { 'mData': 'min',    'sTitle': 'Min'    },
                                    { 'mData': 'peak',   'sTitle': 'Peak'   },
                                    { 'mData': 'max',    'sTitle': 'Max'    },
                                    { 'mData': 'costs',  'sTitle': 'Costs'  },
                                    { 'mData': 'ratio',  'sTitle': 'Risk'   }]
        json_result['errors'] = self.issues['errors']
        json_result['warnings'] = self.issues['warnings']

        return json.dumps(json_result)

