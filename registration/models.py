
from django.db import models


# Create your models here.
from rest_framework.fields import JSONField


class UserProfile(models.Model):
    first_name = models.CharField(max_length=100, blank=False, default='')
    last_name = models.CharField(max_length=100, blank=False, default='')
    nickname = models.CharField(max_length=100, blank=True, default='')
    user_login = models.CharField(max_length=100, blank=True, default='')


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, blank=False, default='')
    role = models.CharField(max_length=100, blank=True, default='')
    user_profile = []


class UserGroup(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    permission = models.CharField(max_length=100, blank=False, default='')
    users = []


class UserHierarchyWrapper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    hierarchy_rank = models.IntegerField(default=1)
    # veto_list = JSONField()
    veto_list = []


class Hierarchy(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    users = []

