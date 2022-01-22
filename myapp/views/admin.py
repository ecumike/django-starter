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
from django.utils.text import capfirst


from ..models import *
from ..forms import *
import myapp.helpers as helpers


def getAdminBreadcrumbs():
	breadcrumbs = [
		{
			'text': 'My app',
			'url': reverse('myapp:home')
		},
		{
			'text': 'Admin center',
			'url': reverse('myapp:admin_home')
		}
	]
	return breadcrumbs




##
##	/myapp/admin/
##
##	Admin home.
##
@user_passes_test(helpers.hasAdminAccess)
def admin_home(request):
	
	breadcrumbs = [
		{
			'text': 'My app',
			'url': reverse('myapp:home')
		},
	]
	
	context = {
		'breadcrumbs': breadcrumbs,
		'counts': {
			'admins': User.objects.filter(groups__name='admins').count(),
		},
		'dataAudits': {}
	}
	
	response = render(request, 'myapp/admin_home.html', context)
	
	helpers.clearPageMessage(request)
	
	return response


##
##	/myapp/admin/adminaccess/
##
##	Manage who is in admin group (Admin access control).
##
@user_passes_test(helpers.hasAdminAccess)
def admin_adminaccess(request):
	breadcrumbs = getAdminBreadcrumbs()
		
	context = {
		'breadcrumbs': breadcrumbs,
		'adminUsers': User.objects.filter(groups__name='admins').order_by('profile__full_name'),
	}
	
	return render(request, 'myapp/admin_adminaccess.html', context)






