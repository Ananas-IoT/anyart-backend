from djongo import models


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

    #restrictions = models.ListField(verbose_name='restriction_list', null=True)
