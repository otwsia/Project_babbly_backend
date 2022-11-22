from django.db import models
import uuid
from datetime import datetime
from app_profiles.models import Profile

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, blank=True, null=True)
    user = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to='post_images/')
    caption = models.TextField(max_length=280, blank=True, null=True)
    repost = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    profile_img = models.CharField(max_length=300, default='blank-profile-picture.png')

    created_at = models.DateTimeField(auto_now_add=True)
    no_of_replies = models.IntegerField(default=0)
    no_of_likes = models.IntegerField(default=0)
    no_of_reposts = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class Reply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    reply_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=15, blank=True, null=True)
    user = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to='post_images/')
    caption = models.TextField(max_length=280)
    og_post = models.CharField(max_length=15, null=True, blank=True)
    profile_img = models.CharField(max_length=300, default='blank-profile-picture.png')

    created_at = models.DateTimeField(auto_now_add=True)
    no_of_replies = models.IntegerField(default=0)
    no_of_likes = models.IntegerField(default=0)
    no_of_reposts = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class Like(models.Model):
    post_id = models.CharField(max_length=300)
    handle = models.CharField(max_length=100)

    def __str__(self):
        return self.handle
