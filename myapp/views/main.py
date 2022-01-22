import io
import requests
import sys

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Value, Q
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string


from ..models import *
from ..forms import *
import myapp.helpers as helpers


##
##	/myapp/
##
##	My app home page.
##
def home(request):
	context = {
		## Nothing yet.
	}
	
	response = render(request, 'myapp/home.html', context)
	helpers.clearPageMessage(request)
	return response	
	
	
	
########################################################
########################################################
##
## Standards views in each app, direct copy/paste.
##
########################################################
########################################################

##
##	/myapp/signin/
##
##	Sign in page
##
def signin(request):
	## If user is already signed in they don't need to be here, so redirect them to home page.
	if request.user.is_authenticated:
		response = redirect(reverse('myapp:home'))
	
	elif request.method == 'GET':
		response = render(request, 'signin.html', {
			'form': AuthenticationForm,
		})
	
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		# NOTE: This ensures all usernames/emails to be lowercase. Prevents mismatch
		# for users with mix-case emails.
		try:
			user = authenticate(request, username=username.lower(), password=password)
		except Exception as ex:
			context = {
				'form': AuthenticationForm,
				'error': 'Uh oh, we were unable to authenticate you because we got an error trying to connect to w3 authentication.<br>You may want to check <a href="https://w3.ibm.com/help/#/outages" target="_blank">w3 outages</a> for status.',
			}
			
			return render(request, 'signin.html', context)
		
		## Success
		if user is not None:
			login(request, user)
			
			# Hit bluepages APIs via w3 Bluemix proxy app and create their profile.
			helpers.updateUserProfile(user)
			
			# Send them back to the page they originally went to before they had to sign in.
			response = redirect(request.POST.get('next', reverse('myapp:home')))
		
		## Fail
		else:
			context = {
				'form': AuthenticationForm,
				'error': 'DOH! It seems your ID/PW combination wasn\'t quite right.<br>Please try again.',
			}
			response = render(request, 'signin.html', context)
	
	return response


##
##	/myapp/signout/
##
##	Signs the user out.
##
def signout(request):
	logout(request)
	return render(request, 'signout.html', {})


##
##	404
##
##	This is only needed if you want to do custom processing when a 404 happens.
##
def custom_404(request, exception):
	referer = request.META.get('HTTP_REFERER', 'None')

	if request.user.username:
		userCaused = '\n*User:* {}'.format(request.user.username)
	else: 
		userCaused = ''	

	if request.get_host() in referer:
		helpers.sendSlackAlert(404, '*Requested path:*  {}\n*Referring page:*	 {}{}'.format(request.path, referer, userCaused))
		
	return render(request, '404.html', {}, status=404)
	

##
##	500
##
##	This is only needed if you want to do custom processing when a 500 happens.
##
def custom_500(request):
	exctype, value = sys.exc_info()[:2]
	
	errMsg = value or '(No error provided)'
	errMsg = str(errMsg)
		
	referer = request.META.get('HTTP_REFERER', 'None')

	if request.user.username:
		userCaused = '\n*User:* {}'.format(request.user.username)
	else: 
		userCaused = ''	

	helpers.sendSlackAlert(500, '*Requested path:*	{}{}\n*Error msg:*	{}\nCheck email for full debug.'.format(request.path, userCaused, errMsg))
		
	return render(request, '500.html', {}, status=500)
	



