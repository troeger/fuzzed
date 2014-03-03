from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from configuration import Configuration
from graph import Graph

class Result(models.Model):
  """
  Class: Project
  
  Fields:
   {Configuration}   configuration  -
   {Graph}           graph          -
   {str}             type           -
   {str}             prob           -
   {int}             prob_sortable  - 
   {int}             decomposition  -
   {str}             issues         -
   {int}             rounds         -
   {int}             failures       -
                               
  """
  
  class Meta:
      app_label = 'FuzzEd'
  
  ANALYSIS_TYPES = [('S','Simulation'),('A','Analysis')]
  
  config        = models.ForeignKey(Configuration, related_name='result')
  graph         = models.ForeignKey(Graph, related_name='results')
  type          = models.CharField(max_length=1, choices= ANALYSIS_TYPES)
  prob          = models.TextField()
  prob_sort     = models.IntegerField() 
  decomposition = models.IntegerField()
  issues        = models.TextField()
  rounds        = models.IntegerField()
  failures      = models.IntegerField()
  
  def __init__ (self, config, graph, type, prob, prob_sort, decomposition, issues, rounds, failures ):
      self.config        = config
      self.graph         = graph
      self.analysis_type = type
      self.prob          = prob
      self.prob_sort     = prob_sort
      self.decomposition = decomposition
      self.issues        = issues
      self.rounds        = rounds
      self.failures      = failures
      
      
  @classmethod                                                
  def createFromXML(self, data):                              
      print '!!!begin_parseXMLResult!!!\n\n'
      print data     
      print '!!!end_parseXMLResult!!!\n\n'
      
      return
      #return cls(..., ..., ..., )
 
  
  
 