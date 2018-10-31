from django.db import models


# Create your models here.

class Limitation(models.Model):
    authority = models.IntegerField(blank=False)
    reason = models.CharField(max_length=100, blank=False, default='')
    restrictions = models.CharField(max_length=100, blank=True, default='')


class Location(models.Model):
    position = models.FloatField()
    restrictions = models.ForeignKey(Limitation, on_delete=models.CASCADE)




