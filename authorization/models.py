from django.contrib.auth.models import User
from django.db import models

USER_RIGHTS = (
    'gov',
    'artist',
    'basic',
)


class UserProfile(models.Model):
    owner = models.OneToOneField('auth.User', on_delete=models.CASCADE, blank=False, related_name='profile',
                                 default=None)
    first_name = models.CharField(max_length=100, blank=False, default='')
    last_name = models.CharField(max_length=100, blank=False, default='')
    rights = models.CharField(max_length=100, blank=False, default='basic')


