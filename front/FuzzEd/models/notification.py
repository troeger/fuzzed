from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):

    class Meta:
        app_label = 'FuzzEd'

    title = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    text = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.title)
