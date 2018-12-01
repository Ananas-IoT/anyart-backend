from djongo import models

from approval.models import CustomLimitation, Hierarchy
from django.contrib.auth.models import User


# Approvable
class PhotoUpload(models.Model):
    photo = models.TextField(verbose_name='Uploaded image')
    location = models.ForeignKey('map.Location', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='photo_uploads')
    description = models.TextField(max_length=500, blank=False, default='')


# Approvable
class Sketch(models.Model):
    workload = models.ForeignKey('upload.Workload', on_delete=models.CASCADE, default=None, blank=True)
    img = models.ImageField('Uploaded sketch', default=None)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sketches', default=None)
    sketch_status = models.CharField(max_length=100, blank=True, default='')
    restrictions = models.ListField(verbose_name='sketch_restrictions', null=True)
    votes = models.ListField(verbose_name='sketch_votes', null=True)


# Approvable
class ArtWork(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    photo_after = models.ImageField(verbose_name='Completed work')
    requirements = models.TextField(max_length=500)
    sketch = models.ForeignKey('upload.Sketch', on_delete=models.CASCADE, related_name='art_work', null=True)
    permission_letter_url = models.FileField(blank=True)
    legal_agreement_url = models.FileField(blank=True)


class Workload(models.Model):
    photo_upload = models.ForeignKey('upload.PhotoUpload', max_length=500, blank=False, on_delete=models.CASCADE)
    work_status = models.CharField(max_length=50, blank=False, default='initialized')
    complete_work = models.BooleanField(default=False, blank=True)
    generic_status = models.CharField(max_length=100, blank=False, default='initialized')
    art_permission = models.FileField()


