from django.contrib.auth.models import User
from django.db import models


class Vote(models.Model):
    user = User
    vote = models.IntegerField(blank=False)
    timestamp = models.DateTimeField()


class GovernmentVote(models.Model):
    vote = models.IntegerField(blank=False)
    timestamp = models.DateTimeField()

