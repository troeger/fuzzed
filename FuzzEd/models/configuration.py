from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from graph import Graph

class Configuration(models.Model):
  """
  Class: Project
  
  Fields:
   {Graph} graph       -        
   {int}   costs       -                    
  """
  
  class Meta:
      app_label = 'FuzzEd'
  
  graph  = models.ForeignKey(Graph, related_name='configurations')
  costs  = models.IntegerField()
