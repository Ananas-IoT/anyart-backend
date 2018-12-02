import base64
from json import loads, dumps

from django.contrib.auth.models import User
from geopy import Nominatim
from rest_framework import serializers

from map.checks import check
from map.models import Limitation, Location, Workload, PhotoUpload


class LimitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limitation
        fields = ('id', 'authority', 'reason', 'restriction')

    def create(self, validated_data):
        limitation = Limitation.objects.create(**validated_data)
        return limitation


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'lat', 'lng', 'street_address', 'restrictions')

    def create(self, validated_data):
        print(validated_data)
        geolocator=Nominatim()
        try:
            restrictions = validated_data.pop('restrictions')
            validated_data.pop('company')
        except KeyError:
            pass

        try:
            validated_data['lat']
        except KeyError:
            validated_data['lat'] = 0

        if validated_data['lat'] > 0:
            print(validated_data)
            location = geolocator.reverse([validated_data['lat'], validated_data['lng']])
            print(location.address)
            validated_data['street_address'] = location.address
        else:
            geolocator = Nominatim()
            location = geolocator.geocode([validated_data['street_address']])
            print(location.address)
            print(location.latitude, location.longitude)
            validated_data['lat'] = location.latitude
            validated_data['lng'] = location.longitude
        for track_data in restrictions:
            Limitation.objects.create(location=location, **track_data)
        print(validated_data)
        location = Location.objects.create(**validated_data)

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


class PhotoUploadSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.ImageField(required=True)
    photo_upload_id = serializers.IntegerField(required=True)

    class Meta:
        model = PhotoUpload
        fields = ('photo', 'photo_upload_id')

    def encode(self, photo):
        data = base64.b64encode(photo.read())
        return data

    def create(self, validated_data):
        photo_file = validated_data.get('photo')
        photo_string = self.encode(photo_file)
        photo_id = validated_data.get('photo_upload_id')

        photo_upload = PhotoUpload.objects.filter(id=photo_id, photo=photo_string)

        photo_upload.save()

        return photo_upload


class ReadOnlyPhotoUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoUpload
        fields = ('photo', 'owner', 'description', 'location', 'id')
        read_only_fields = ('photo', 'owner', 'description', 'location', 'id')


class WorkloadSerializer(serializers.HyperlinkedModelSerializer):
    work_status = serializers.CharField(required=False)
    generic_status = serializers.CharField(required=False)
    art_permission = serializers.CharField(required=False)
    photo_upload = ReadOnlyPhotoUploadSerializer(required=False)
    location = LocationSerializer(required=True, many=False)

    class Meta:
        model = Workload
        fields = ('work_status', 'generic_status', 'art_permission', 'photo_upload', 'location')

    # def validate_location(self, value):


    def create(self, validated_data):
        photo_upload_data = validated_data.pop('photo_upload')
        location_data = validated_data.pop('location')

        workload = Workload.objects.create(**validated_data)

        photo_upload_data['workload'] = workload

        location_serializer = LocationSerializer()
        location = location_serializer.create(location_data)

        photo_upload_data['location'] = location
        token = self.context.get('token')
        owner = User.objects.filter(id=token).get()
        photo_upload_data['owner'] = owner

        photo_upload = PhotoUpload.objects.create(**photo_upload_data)

        return workload

class ReadOnlyWorkloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workload
        fields = ('id', 'work_status', 'generic_status', 'created')
        read_only_fields = ('id', 'work_status', 'generic_status', 'created')