from django.db import models

# Create your models here.
from authorization.models import User


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField(blank=False)
    timestamp = models.DateTimeField()


class GovernmentVote(models.Model):
    vote = models.IntegerField(blank=False)
    timestamp = models.DateTimeField()

