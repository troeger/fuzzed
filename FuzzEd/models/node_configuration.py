from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from FuzzEd.lib.jsonfield import JSONField
from node import Node
from configuration import Configuration

class NodeConfiguration(models.Model):
  """
  Class: Project
  
  Fields:
   {Node}          node            
   {JSON}          setting                        
   {Configuration} configuration                
  """
  
  class Meta:
      app_label = 'FuzzEd'
  
  node          = models.ForeignKey(Node)
  setting       = JSONField()
  configuration = models.ForeignKey(Configuration, related_name='node_configurations')