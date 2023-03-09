from django.contrib import admin

# Register your models here.

from .models import User, Record

admin.site.register(User)
admin.site.register(Record)