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
    user = models.OneToOneField(auth.User, related_name='profile')
    newsletter = models.BooleanField(default=False)

    class Meta:
        app_label = 'ore'

# handler that automatically creates a new user profile when also a new django user is created
# This breaks on fresh database creation, since the signal is triggered when no UserProfile
# table was created so far. For this reason, we silently ignore all errors
# here.


@receiver(post_save, sender=auth.User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserProfile.objects.get_or_create(user=instance)
        except Exception:
            pass


# ensures that only the UserProfile is visible when importing this module
__all__ = ['UserProfile']
