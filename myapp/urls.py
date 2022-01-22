"""
	myapp app URL Configuration

"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from .views import *


## All URLs are namespaced in root URL config with "myapp"
urlpatterns = [
	
	## Pages
	url(r'^$', home, name='home'), 	
	
	## Admin URLs
	url(r'^admin/$', admin_home, name='admin_home'),
	url(r'^admin/adminaccess/$', admin_adminaccess, name='admin_adminaccess'),
		
	## APIs.
	url(r'^api/user/add/$', api_user_add, name='api_user_add'),
	url(r'^api/adminaccess/$', api_adminaccess, name='api_adminaccess'),
		
	## Sign in/out.
	url(r'^signin/$', signin, name='signin'),
	url(r'^signout/$', signout, name='signout'),

	# Dev test only.
	url(r'^403/$', TemplateView.as_view(template_name="403.html"), name='test403'),
	url(r'^404/$', TemplateView.as_view(template_name="404.html"), name='test404'),
	url(r'^500/$', TemplateView.as_view(template_name="500.html"), name='test500'),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

## DEBUG is in root URL file.
