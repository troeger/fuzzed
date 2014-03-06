from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from graph import Graph
from configuration import Configuration
from job import Job
from FuzzEd.models import xml_analysis, xml_simulation

class Result(models.Model):
  """
  Class: Project
  
  Fields:
   {Configuration}   configuration  -
   {Graph}           graph          -
   {str}             type           -
   {str}             prob           -
   {int}             prob_sort      - 
   {int}             decomposition  -
   {str}             issues         -
   {int}             rounds         -
   {int}             failures       -
                               
  """
  
  class Meta:
      app_label = 'FuzzEd'
  
  ANALYSIS_TYPES = [('S','Simulation'),('A','Analysis')]
  
  graph         = models.ForeignKey(Graph, related_name='results')
  configuration = models.OneToOneField(Configuration, primary_key=True, related_name='result')
  type          = models.CharField(max_length=1, choices= ANALYSIS_TYPES)
  prob          = models.TextField()
  prob_sort     = models.IntegerField() 
  decomposition = models.IntegerField()
  node_issues   = models.TextField()
  rounds        = models.IntegerField()
  failures      = models.IntegerField()
  
  def __init__ (self, configuration, graph, type, prob, prob_sort, decomposition, issues, rounds, failures ):
      self.configuration = configuration
      self.graph         = graph
      self.type          = type
      self.prob          = prob
      self.prob_sort     = prob_sort
      self.decomposition = decomposition
      self.node_issues   = issues
      self.rounds        = rounds
      self.failures      = failures
      
      
  @classmethod                                                
  def createFromXML(self, data, kind, graph):                              
      print '!!!begin_parseResult!!!\n\n'
      
      type   = kind
      graph_issues = {'errors':{}, 'warnings':{} }
      prob   = {}
          
      
      assert(data)
      result_data = str(data)
      topId = graph.top_node().client_id
      
      if (kind == Job.TOP_EVENT_JOB):
          doc = xml_analysis.CreateFromDocument(result_data)
      elif (kind == Job.SIMULATION_JOB):
          doc = xml_simulation.CreateFromDocument(result_data)
      else:
          assert(False)
      
      ## Check global issues that are independent from the particular configuration
      ## Since the frontend always wants an elementID, we stitch them
      ## to the TOP event for the moment (check issue #181)
      ## TODO: This will break for RBD analysis, since there is no top event
      if hasattr(doc, 'issue'):
          graphErrors = []
          graphWarnings = []
          for issue in doc.issue:
              if issue.message and len(issue.message)>0:
                  if issue.isFatal:
                      graphErrors.append(issue.message)
                  else:
                      graphWarnings.append(issue.message)
          if len(graphErrors) > 0:
              graph_issues['errors'][topId] = graphErrors
          if len(graphWarnings) > 0:
              graph_issues['warnings'][topId] = graphWarnings
               
               
      results = doc.result
          
      #TODO:  This will move to a higher XML hierarchy level in an upcoming schema update
      if hasattr(results[0], 'decompositionNumber'):
          decomposition = str(results[0].decompositionNumber)
      
      
      #TODO: Save all configurations
      #for result in results:
      
      
      
      
      print 'graph_issues:  ' + str(graph_issues)
      print 'decomposition: ' + str(decomposition)
      print 'prob:          ' + str(prob)
      
      print '!!!end_parseResult!!!\n\n'
      return
 
  
  
 