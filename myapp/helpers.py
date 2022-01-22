import ast
import base64
import io
import json
import os
import requests


from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.crypto import get_random_string

from copy import copy



# User extension for access control used in decorator functions and templates
#  to easily restrict view access and template functionality.
def hasAdminAccess(user):
	"""
	User is Superuser or member of the admin group.
	"""
	try:
		hasAccess = user.is_superuser or user.groups.filter(name='admins').exists()
	except:
		hasAccess = False
	
	return hasAccess   

# Add decorator methods to User object so they are automatically available anywhere, even in templates!
# No need to pass this in thru views. 
# Template example usage: {% if request.user.hasAdminAccess %}
# View decorator usage:	 @user_passes_test(helpers.hasAdminAccess)
User.add_to_class('hasAdminAccess', hasAdminAccess)


def setPageMessage(request, msgType, msgText):
	"""
	Sets the session page message
	"""
	msgClass = "green" if msgType == "success" else "dark-red"
	
	request.session['pageMessage'] = {
		'class': msgClass,
		'text': msgText,
	}

	
def clearPageMessage(request):
	"""
	Clears the session page message
	"""
	request.session['pageMessage'] = None

	
def sendSlackAlert(errorCode, msg):
	"""
	Takes the HTTP error code passed and the message and pushes a message to the Slack web hook URL for our room.
	"""
	slackUrl = settings.SLACK_ALERT_URL
	icon = ':error:' if errorCode > 499 else ':warning:'
	
	payload = {
		'username': 'My app',
		'icon_emoji': icon,
		'text': '*A {} error just happened*\n{}'.format(errorCode, msg),
	}
	
	if slackUrl:
		r = requests.post(slackUrl, json=payload)


def sendEmail(emailData):
	returnData = None
	
	try:
		# DEV DEBUG - Only send to me. Comment out when ready for production.
		#emailData['recipients'] = ['santelia@us.ibm.com']
		returnData = send_mail(emailData['subject'], '<font face="sans-serif" size="2">{}</font>'.format(emailData['message']), 'do-not-reply@ibm.com', emailData['recipients'], html_message='<font face="sans-serif" size="2">{}</font>'.format(emailData['message']), fail_silently=True)
		
	except Exception as ex:
		pass
	
	return returnData
	

def updateUserProfile(user):
	"""
	User profile is created on user.create, so we know user.profile exists when this is called.
	Fetches full name of user when the sign in. If user has name-change, 
	just have them sign out and sign in and it'll get updated.
	Since we keep persistent sign-in state we can keep this set on every sign in.
	"""
	user.profile.full_name = user.username
	
	if 'ibm.com' in user.username:
		try:
			r = requests.get(
				f'https://unified-profile-api.us-south-k8s.intranet.ibm.com/v3/profiles/{user.username.lower()}/profile',
				timeout=5
			)
			user.profile.full_name = r.json()["content"]["identity_info"]["nameFull"]
		except Exception as ex:
			pass
	
	user.save()


def createNewUser(email):
	emailLower = email.lower()

	user, created = User.objects.get_or_create(
		username = emailLower,
		defaults = {
			'email': emailLower,
			'password': get_random_string()
		}
	)
	
	# Profile is automatically created via user.save() signal.
	# Now update their profile via bluepages APIs.
	updateUserProfile(user)
	
	return user
	
	