
from django.db import models




# class UserProfile(models.Model):
#     first_name = models.CharField(max_length=100, blank=False, default='')
#     last_name = models.CharField(max_length=100, blank=False, default='')
#     nickname = models.CharField(max_length=100, blank=True, default='')
#     user_login = models.CharField(max_length=100, blank=True, default='')


class UserGroup(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    permission = models.CharField(max_length=100, blank=False, default='')
    users = []


# class UserHierarchyWrapper(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
#     hierarchy_rank = models.IntegerField(default=1)
#     veto_list = []
#
#
# class Hierarchy(models.Model):
#     name = models.CharField(max_length=100, blank=False, default='')
#     users = []

