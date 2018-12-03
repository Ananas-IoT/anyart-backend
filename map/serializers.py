import base64
from json import loads, dumps

from django.contrib.auth.models import User
from geopy import Nominatim
from rest_framework import serializers

from map.checks import check
from map.models import Limitation, Location, Workload, PhotoUpload, Sketch


class LimitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limitation
        fields = ('id', 'authority', 'reason', 'restriction')

    def create(self, validated_data):
        return Limitation.objects.create(**validated_data)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'lat', 'lng', 'street_address', 'restrictions')

    def create(self, validated_data):
        print(validated_data)
        geolocator = Nominatim()
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
            try:
                restriction_qs = Limitation.objects.filter(id=restriction['id'])
                # print(restriction['id'])
            except:
                restriction_qs = Limitation.objects.filter(id=restriction)
                # print(restriction)

            print(restriction_qs)

            if restriction_qs.exists():
                restriction = restriction_qs.first()
                # print("re")
                # print(restriction)
            else:
                # print('yes')
                restriction = LimitationSerializer.create(**restriction)
                # print("rek")
                # print(restriction)
            instance.restrictions.add(restriction)
        print("is")
        print(instance)
        return instance

    def create_limitations(self, validated_data):

        serializer = LocationSerializer(self)
        # print(serializer.data)
        print(validated_data)

        serializer.data['restrictions'].append(validated_data)
        s = serializer.data
        # print(s)
        return serializer.data

    def add_limitation(serializer, location, restriction):
        try:
            id = int(restriction['id'])
        except KeyError:
            id = 0

        if id > 0:
            # print(restriction['id'])
            # restrictions = LimitationSerializer(Limitation.objects.filter(id=restriction['id']).first()).data
            restrictions = restriction['id']
        else:
            print(restriction)
            restrictions = LimitationSerializer(data=restriction)
            print(restrictions.is_valid())
            if restrictions.is_valid():
                restrictions.save()
                restrictions = restrictions.data

        # print(restrictions.data)

        location_new = LocationSerializer.create_limitations(location, restrictions)

        serializer = LocationSerializer(serializer.update(location, location_new))

        return serializer

    def check_in_api(self):
        # print(self.data)
        address_data = self.data['street_address'].split(', ')

        # print(address_data)
        address_building = float(address_data[0])
        address_street = address_data[1].split()[0]
        print(address_building)
        print(address_street)

        restriction_list = check(address_building, address_street)

        return restriction_list


class PhotoUploadSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.ImageField(required=False)
    photo_upload_id = serializers.IntegerField(required=False)

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
    location = LocationSerializer(required=False, many=False)

    class Meta:
        model = Workload
        fields = ('work_status', 'generic_status', 'art_permission', 'photo_upload', 'location')

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


class SketchSerializer(serializers.HyperlinkedModelSerializer):
    workload_id = serializers.IntegerField(required=True)
    img = serializers.FileField()

    class Meta:
        model = Sketch
        fields = ('workload_id', 'owner', 'img', 'sketch_status', 'created')
        required_fields = ('workload_id',)

    def encode(self, photo):
        data = base64.b64encode(photo.read())
        return data

    def create(self, validated_data):
        token = self.context.get('token')
        owner = User.objects.filter(id=token).get()
        validated_data['owner'] = owner

        file = validated_data.pop('img')
        file_string = self.encode(file)
        validated_data['img'] = file_string

        sketch = Sketch.objects.create(**validated_data)

        return sketch


class SketchReadOnlySerializer(serializers.ModelSerializer):
    # ('workload', 'sketch_status', 'created', 'owner', 'img', 'id')
    class Meta:
        model = Sketch
        fields = '__all__'
        read_only_fields = ('workload', 'sketch_status', 'created', 'owner', 'img', 'id')
