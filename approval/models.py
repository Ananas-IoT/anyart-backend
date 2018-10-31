from django.db import models

# Create your models here.
from registration.models import Hierarchy


class CustomLimitation(models.Model):
    limitation_name = models.CharField(max_length=100, blank=False, default='')
    authority_name = models.CharField(max_length=100, blank=False, default='')
    explanation = models.TextField(max_length=500, blank=False, default='')


class ApprovalGroup(models.Model):
    hierarchy = models.ForeignKey(Hierarchy, limit_choices_to={'name': 'Government'}, on_delete=models.CASCADE)


class Veto(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    veto_rank = models.IntegerField()
