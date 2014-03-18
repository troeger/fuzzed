from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from graph import Graph
from configuration import Configuration
from FuzzEd.models import xml_analysis, xml_simulation
from FuzzEd.lib.jsonfield import JSONField

class Result(models.Model):
  """
  Class: Project
  
  Fields:
   {Configuration}   configuration  -
   {Graph}           graph          -
   {str}             type           -
   {JSON}            prob           -
   {int}             prob_sort      - 
   {int}             decomposition  -
   {JSON}            node_issues    -
   {int}             rounds         -
   {int}             failures       -
                               
  """
  
  class Meta:
      app_label = 'FuzzEd'
  
  ANALYSIS_TYPES = [('S','Simulation'),('A','Analysis')]
  
  graph         = models.ForeignKey(Graph, related_name='results')
  configuration = models.OneToOneField(Configuration, primary_key=True, related_name='result')
  type          = models.CharField(max_length=1, choices= ANALYSIS_TYPES)
  prob          = JSONField()
  prob_sort     = models.IntegerField() 
  decomposition = models.IntegerField()
  node_issues   = JSONField()
  rounds        = models.IntegerField()
  failures      = models.IntegerField()
  
  