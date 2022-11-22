from django.db import models
from administration.models import Account

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    name = models.CharField(max_length=15, blank=True, null=True)
    handle = models.CharField(max_length=15, unique=True)
    id_user = models.AutoField(primary_key=True)

    bio = models.TextField(max_length=160, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    profile_img = models.ImageField(blank=True, null=True, upload_to="profile_images/", default='blank-profile-picture.png')
    banner_img = models.ImageField(blank=True, null=True, upload_to="banner_images/", default='default-bg.jpeg')
    website = models.CharField(max_length=30, blank=True, null=True)

    date_joined = models.DateField(auto_now_add=True)
    no_of_followers = models.IntegerField(default=0)
    no_of_posts = models.IntegerField(default=0)
    def __str__(self):
        return self.handle

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user