from django.contrib.auth.models import User
from django.db import models


class Vote(models.Model):
    sketch = models.ForeignKey('upload.Sketch', on_delete=models.CASCADE, null=True),
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    vote = models.IntegerField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class GovernmentVote(models.Model):
    perspective_object = models.ForeignKey('approval.')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    vote = models.IntegerField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

