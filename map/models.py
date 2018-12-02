from djongo import models

from approval.models import CustomLimitation, Hierarchy
from django.contrib.auth.models import User


class Limitation(models.Model):
    id = models.AutoField(blank=False, primary_key=True)
    authority = models.IntegerField(blank=False)
    reason = models.CharField(max_length=100, blank=False, default='')
    restriction = models.CharField(max_length=100, blank=True, editable=True)


class Location(models.Model):
    lat = models.FloatField(null=True, blank=True, editable=True)
    lng = models.FloatField(null=True, blank=True, editable=True)
    street_address = models.CharField(max_length=200, blank=True)

    restrictions = models.ManyToManyField(Limitation, blank=True)



# Approvable
class PhotoUpload(models.Model):
    workload = models.ForeignKey('map.Workload', max_length=500, blank=False, on_delete=models.CASCADE)
    location = models.ForeignKey('map.Location', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='photo_uploads')
    photo = models.TextField(verbose_name='Uploaded image', blank=True)
    description = models.TextField(max_length=500, blank=False, default='')
    created = models.DateTimeField(auto_now_add=True)


# Approvable
class Sketch(models.Model):
    workload = models.ForeignKey('map.Workload', on_delete=models.CASCADE, default=None, blank=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sketches', default=None)
    img = models.TextField('Uploaded sketch', default=None)
    sketch_status = models.CharField(max_length=100, blank=True, default='uploaded')
    # restrictions = models.ListField(verbose_name='sketch_restrictions', null=True)
    # votes = models.ListField(verbose_name='sketch_votes', null=True)
    created = models.DateTimeField(auto_now_add=True)



# Approvable
class ArtWork(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    sketch = models.ForeignKey('map.Sketch', on_delete=models.CASCADE, related_name='art_work', null=True)
    photo_after = models.TextField(verbose_name='Completed work')
    requirements = models.TextField(max_length=500)
    permission_letter_url = models.FileField(blank=True)
    legal_agreement_url = models.FileField(blank=True)
    created = models.DateTimeField(auto_now_add=True)



class Workload(models.Model):
    work_status = models.CharField(max_length=50, blank=False, default='initialized')
    generic_status = models.CharField(max_length=100, blank=False, default='initialized')
    art_permission = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

