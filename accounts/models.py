from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('user', 'User'),
        ('public', 'Public'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='public')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


