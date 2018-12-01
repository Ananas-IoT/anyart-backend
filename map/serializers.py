from json import loads, dumps

from rest_framework import serializers

from map.checks import check
from map.models import Limitation, Location


class LimitationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Limitation
        fields = ('id', 'authority', 'reason', 'restriction')

    def create(self, validated_data):
        limitation = Limitation.objects.create(**validated_data)
        return limitation

class LocationSerializer(serializers.ModelSerializer):
    restrictions = LimitationSerializer(many=True, )


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'lat', 'lng', 'street_address', 'restrictions')

    def create(self, validated_data):
        restrictions = validated_data.pop('restrictions')
        location = Location.objects.create(**validated_data)
        for track_data in restrictions:
            Limitation.objects.create(location=location, **track_data)
        return location

    def update(self, instance, validated_data):
        restrictions_data = validated_data.pop('restrictions')

        restrictions = instance.restrictions.all()
        restrictions = list(restrictions)
        print("restrictions", end=" ")
        print(restrictions)
        print(restrictions_data)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lng = validated_data.get('lng', instance.lng)
        instance.street_address = validated_data.get('street_address', instance.street_address)
        instance.save()

        for restriction in restrictions_data:
            print(restriction)
            # try:
            restriction_qs = Limitation.objects.filter(id=restriction['id'])
            print(restriction['id'])
            # except:
            #     restriction_qs = Limitation.objects.filter(id=restriction.id)
            #     print(restriction.id)
            # print(restriction_qs)

            if restriction_qs.exists():
                restriction = restriction_qs.first()
                print("re")
                print(restriction)
            else:
                print('yes')
                restriction = LimitationSerializer.create(**restriction)
                print("re")
                print(restriction)
            instance.restrictions.add(restriction)
        print(instance)

    def create_limitations(self, validated_data):
        print(validated_data.data)
        limitations = validated_data.data
        old = Location.objects.get(pk=self.initial_data['id'])
        print(old)

        self.initial_data['restrictions'].append(limitations)
        s = self.initial_data
        print(s)
        serializer = LocationSerializer(data=self.initial_data)
        serializer.update(old, loads(dumps(s)))
        return serializer

    def check_in_api(self):
        print(self.data)
        address_data = self.data['street_address'].split(', ')

        print(address_data)
        address_building = float(address_data[0])
        address_street = address_data[1].split()[0]
        print(address_building)
        print(address_street)

        error_list = check(address_building, address_street)
        return error_list

