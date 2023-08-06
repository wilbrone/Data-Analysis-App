from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class Sessions(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.now)
    date_modified = models.DateField(default=datetime.now)

class Messages(models.Model):
    session_id = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    human = models.TextField()
    ai = models.TextField()
    created_at = models.DateField(default=datetime.now)
    date_modified = models.DateField(default=datetime.now)