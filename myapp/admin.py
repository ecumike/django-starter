from django.contrib import admin

from .models import *


# Automatically create the code for this file by running this in the console:
#    ./manage.py admin_generator myapp
# Then just copy/paste the output of all the registered classes below.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'inactive', 'user', 'full_name', 'image')
    list_filter = ('inactive', 'user')


@admin.register(BannerNotification)
class BannerNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active', 'banner_text', 'banner_type')
    list_filter = ('active',)
    search_fields = ('name',)
    
