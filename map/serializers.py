from rest_framework import serializers

from map.models import Limitation, Location


class LimitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limitation
        fields = ('authority', 'reason', 'restrictions')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('position', 'street_address', 'restrictions')
