from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    thumbnail = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)

class Likes(models.Model):
    created_at = models.DateTimeField(default=now)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)

class Notifications(models.Model):
    likes = models.ForeignKey(Likes, on_delete=models.CASCADE, null=True)
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1, default='0')
