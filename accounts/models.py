from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Profile(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.TextField(null=True)
    updated_at = models.DateTimeField(null=True)
