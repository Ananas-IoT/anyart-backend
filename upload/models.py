from django.db import models

# Create your models here.
from approval.models import CustomLimitation
from map.models import Location
# from authorization.models import User, Hierarchy


# class PhotoUpload(models.Model):
#     photo_url = models.URLField(max_length=500, blank=False, default='')
#     location = models.OneToOneField(Location, on_delete=models.CASCADE, primary_key=True, )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     description = models.TextField(max_length=500, blank=False, default='')
#
#
# class Sketch(models.Model):
#     img_url = models.URLField(max_length=500, blank=False, default='')
#     restrictions = models.ForeignKey(CustomLimitation, on_delete=models.CASCADE)
#     artists = models.ForeignKey(Hierarchy, limit_choices_to={'name': 'Artist'},on_delete=models.CASCADE)
#     sketchStatus = models.CharField(max_length=100, blank=True, default='')
#
#
# class Workload(models.Model):
#     photo_upload = models.URLField(max_length=500, blank=False, default='')
#     frontend_status = models.CharField(max_length=100, blank=False, default='')
#     complete_work = models.BooleanField()
#     status = models.CharField(max_length=100, blank=False, default='')
#     art_permission = models.FileField()
#     sketches = []
#
#
# class ArtWork(models.Model):
#     artist_user = []
#     photo_after = models.URLField(max_length=500, blank=False, default='')
#     requirements = models.TextField(max_length=500)
#     sketch = Sketch()
#     permision_letter_url =  models.URLField(max_length=500, blank=False, default='')
#     legal_agreement_url = models.URLField(max_length=500, blank=False, default='')