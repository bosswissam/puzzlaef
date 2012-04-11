from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	location = models.CharField(max_length=200)

	def __unicode__(self):
		return unicode(self.user)
    
def create_user_profile(sender, **kwargs):
    """When creating a new user, make a profile for him or her."""
    u = kwargs["instance"]
    if not UserProfile.objects.filter(user=u):
        UserProfile(user=u).save()

post_save.connect(create_user_profile, sender=User)