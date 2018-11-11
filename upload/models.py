from django.db import models

# Create your models here.
from approval.models import CustomLimitation, Hierarchy
from map.models import Location
from django.contrib.auth.models import User


class PhotoUpload(models.Model):
    photo_url = models.URLField(max_length=500, blank=False, default='')
    location = models.OneToOneField(Location, on_delete=models.CASCADE, primary_key=True, )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=False, default='')


class Sketch(models.Model):
    img_url = models.URLField(max_length=500, blank=False, default='')
    restrictions = models.ForeignKey(CustomLimitation, on_delete=models.CASCADE)
    artists = models.ForeignKey(User, on_delete=models.CASCADE)
    sketchStatus = models.CharField(max_length=100, blank=True, default='')


class Workload(models.Model):
    photo_upload = models.URLField(max_length=500, blank=False, default='')
    frontend_status = models.CharField(max_length=100, blank=False, default='')
    complete_work = models.BooleanField()
    status = models.CharField(max_length=100, blank=False, default='')
    art_permission = models.FileField()
    sketches = []


class ArtWork(models.Model):
    artist_user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_after = models.URLField(max_length=500, blank=False, default='')
    requirements = models.TextField(max_length=500)
    sketch = Sketch()
    permission_letter_url = models.URLField(max_length=500, blank=False, default='')
    legal_agreement_url = models.URLField(max_length=500, blank=False, default='')
