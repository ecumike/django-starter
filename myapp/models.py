from datetime import datetime, timedelta

from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count, Sum, Value, Q
from django.db.models.functions import Lower
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


import cos as cos



########################################################
########################################################
##
## Standards models in each app, direct copy/paste (trim Profile as needed).
##
########################################################
########################################################

class Profile(models.Model):
	"""
	Extension of user object. Receives signal from User obj and 
	creates/saves the user's profile.
	"""
	inactive = models.BooleanField(default=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=255, blank=True)
	image = models.TextField(blank=True, default='')

	
	class Meta:
		ordering = ['full_name']
		
	def __str__(self):
		return '{} : {}'.format(self.user, self.full_name)
	
	def getImage(self):
		if self.image and self.image != 'None':
			return self.image
		else:
			return staticfiles_storage.url('shared/img/unknownuser.png')		

	def getName(self):
		if self.full_name:
			return self.full_name
		else:
			return self.user.username

	def updateFromPost(self, post):
		updatableFields = [
			'full_name',
			'image',
		]
		
		for field in updatableFields:
			postedValue = post.get(field, None)
			
			if postedValue:
				setattr(self, field, postedValue)


# Django signals: Tells Django to automatically save the User's Profile record when User is saved.
# Profile is an extention of User.
# You should never save Profile directly. Update profile fields ('user.profile.fieldABC') and do "user.save()".
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
	

class BannerNotification(models.Model):
	"""
	Allows you to create a site-wide banner at the top of the page for site-wide 
	notifications, i.e. site maintenance, problems, important updates, etc.
	"""
	name = models.CharField(max_length=32)
	active = models.BooleanField(default=False)
	banner_text = models.CharField(max_length=255)
	banner_type = models.CharField(default='info', choices=[
		('info','info'),
		('warn','warn'),
		('alert','alert'),
	], max_length=10)


	class Meta:
		ordering = ['active','name']

	def __str__(self):
		return '%s - %s - %s' % (self.name, self.banner_type, self.active)


