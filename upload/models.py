from django.db import models

# Create your models here.
from approval.models import CustomLimitation, Hierarchy
from django.contrib.auth.models import User


class PhotoUpload(models.Model):
    photo = models.ImageField(verbose_name='Uploaded image')
    location = models.OneToOneField('map.Location', on_delete=models.CASCADE, primary_key=True, )
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='photo_uploads')
    description = models.TextField(max_length=500, blank=False, default='')


class Sketch(models.Model):
    img_url = models.URLField(max_length=500, blank=False, default='')
    restrictions = models.ForeignKey('approval.CustomLimitation', on_delete=models.CASCADE)
    artist = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sketches')
    sketchStatus = models.CharField(max_length=100, blank=True, default='')


class Workload(models.Model):
    photo_upload = models.URLField(max_length=500, blank=False, default='')
    frontend_status = models.CharField(max_length=100, blank=False, default='')
    complete_work = models.BooleanField()
    status = models.CharField(max_length=100, blank=False, default='')
    art_permission = models.FileField()
    sketches = []


class ArtWork(models.Model):
    artist_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    photo_after = models.URLField(max_length=500, blank=False, default='')
    requirements = models.TextField(max_length=500)
    sketch = models.OneToOneField('upload.Sketch', on_delete=models.CASCADE, related_name='art_work')
    permission_letter_url = models.FileField(blank=True)
    legal_agreement_url = models.FileField(blank=True)

