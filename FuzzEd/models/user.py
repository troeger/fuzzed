import django.contrib.auth.models as auth
import django.db.models as models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user       = models.OneToOneField(auth.User)
    newsletter = models.BooleanField(default=False)

    class Meta:
        app_label = 'FuzzEd'

@receiver(post_save, sender=auth.User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
