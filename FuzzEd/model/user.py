import django.contrib.auth.models as auth
import django.db.models as models

class UserProfile(models.Model):
	user       = models.OneToOneField(auth.User)
	newsletter = models.BooleanField(default=False)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=auth.User)
