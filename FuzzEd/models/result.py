from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from graph import Graph
from FuzzEd.models import xml_analysis, xml_simulation, Configuration
from FuzzEd.lib.jsonfield import JSONField

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
