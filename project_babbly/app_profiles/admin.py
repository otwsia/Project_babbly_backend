from django.contrib import admin
from .models import Profile, FollowersCount

# Register your models here.
admin.site.register(Profile)
admin.site.register(FollowersCount)