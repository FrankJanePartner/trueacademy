from django.contrib import admin
from .models import Application
from django.contrib.auth.models import Group

admin.site.register(Application)
admin.site.unregister(Group)
