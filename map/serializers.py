from rest_framework import serializers

from map.models import Limitation, Location


class LimitationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Limitation
        fields = ('authority', 'reason', 'restriction')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'lat', 'lng', 'street_address', 'restrictions')