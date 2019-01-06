import logging

from django.contrib.auth.models import User
from django.db import models

from FuzzEd.models import Graph, Project

logger = logging.getLogger('FuzzEd')


class Sharing(models.Model):

    """
    Class: Sharing

    This class models a graph sharing, which represents the fact that a graph owner shared it's graph
    with another user.

    Fields:
     {Graph}       graph       - The graph being shared.
     {User}        user        - The user that got the graph shared by it's owner.
     {datetime}    created     - The time when the graph as shared with the user.
     {Project}     project     - The project that the shared graph belongs to on the non-owner side.
                                 This is initially empty, which demands some handling by the frontend.
    """
    class Meta:
        app_label = 'FuzzEd'

    graph = models.ForeignKey(Graph, related_name='sharings')
    user = models.ForeignKey(User, related_name='sharings')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    project = models.ForeignKey(
        Project,
        null=True,
        default=None,
        related_name='sharings')

    def __unicode__(self):
        return unicode('Graph %u shared with %s by %s.' %
                       (self.graph.pk, self.user, self.graph.owner))
