import django.contrib.auth.models as auth

import django.db.models as models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Class: UserProfile
    
    Extends: models.Model
    
    A user profile that enriches the standard django user with additional information, such as e.g. if he or she wants
    to receive newsletters.
    
    Fields:
     {User} - the wrapped django user
     {bool} - flag indicating whether a newsletter is desired
    """
    user       = models.OneToOneField(auth.User, related_name='profile')
    newsletter = models.BooleanField(default=False)

    class Meta:
        app_label = 'FuzzEd'

# handler that automatically creates a new user profile when also a new django user is created
@receiver(post_save, sender=auth.User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

# ensures that only the UserProfile is visible when importing this module
__all__ = ['UserProfile']
