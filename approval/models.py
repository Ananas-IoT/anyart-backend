from django.contrib.auth.models import User
from django.db import models


class CustomLimitation(models.Model):
    limitation_name = models.CharField(max_length=100, blank=False, default='')
    authority_name = models.CharField(max_length=100, blank=False, default='')
    explanation = models.TextField(max_length=500, blank=False, default='')


class ApprovalGroup(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    hierarchy = []


class Veto(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    veto_rank = models.IntegerField()


class UserHierarchyWrapper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    hierarchy_rank = models.IntegerField(default=1)
    veto_list = []


class Hierarchy(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    users = []

