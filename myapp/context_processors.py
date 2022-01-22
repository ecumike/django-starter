from django.conf import settings # import the settings file

def app_settings(request):
	# return the value you want as a dictionnary. you may add multiple values in there.
	return {
		'DATABASE_HOST': settings.DATABASES['default']['HOST'],
		'BLACKOPS_COS_BUCKET_URL': settings.BLACKOPS_COS_BUCKET_URL,
	}