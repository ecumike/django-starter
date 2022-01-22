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
##	/myapp/api/user/add/ <POST DATA>
##
##	Creates a user with the passed email and name. Basic.
##	Returns the user object ID and user's name (for optional display).
##	Only admins can add users.
##
@user_passes_test(helpers.hasAdminAccess)
def api_user_add(request):
	email = request.POST.get('email')
	name = request.POST.get('name')
	httpCode = 404
	
	# NOTE: This ensures all usernames/emails to be lowercase. Prevents mismatch
	# for users with mix-case emails.
	try:
		user = helpers.createNewUser(email)
		
		httpCode = 200
		responseData = {
			'id': user.id,
			'username': user.profile.full_name
		}
	except Exception as ex:
		httpCode = 500
		responseData = {
			'results': {
				'message': repr(ex)
			}
		}
		
	return JsonResponse(responseData, status=httpCode)
	

##
##	/myapp/api/adminaccess/<POST>
##
##	Add/remove a user from the admin group.
##
@user_passes_test(helpers.hasAdminAccess)
def api_adminaccess(request):
	email = request.POST.get('email')
	action = request.POST.get('action')
	adminGroup, created = Group.objects.get_or_create(name='admins')
	httpCode = 404
	
	# If user no existy, throw back default 404.
	try:
		user = User.objects.get(username=email)
	except Exception as ex:
		responseData = {
			'results': {
				'message': repr(ex)
			}
		}
		
	if user:
		if action == "add":
			user.groups.add(adminGroup) 
			httpCode = 200
			responseData = {
				'results': {
					'id': user.id,
					'name': user.profile.full_name,
					'username': user.username
				}
			}
		elif action == "remove":
			adminGroup.user_set.remove(user)
			httpCode = 200
			responseData = {
				'results': {
					'message': 'User removed successfully'
				}
			}
		else:
			httpCode = 400
			responseData = {
				'results': {
					'message': 'You forgot to tell me what to do; add or remove the user.'
				}
			}
		
	return JsonResponse(responseData, status=httpCode)


