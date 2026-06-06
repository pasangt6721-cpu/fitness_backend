# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, help_text="Short bio about yourself")
    profile_picture = models.URLField(blank=True, null=True, help_text="URL to profile image")
    # You can add more fields later: age, weight, height, etc.
    
    def __str__(self):
        return self.username