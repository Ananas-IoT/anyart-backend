from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from upload.models import PhotoUpload, Sketch, Workload, ArtWork
import base64


class PhotoUploadSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.ImageField(required=True)

    class Meta:
        model = PhotoUpload
        fields = ('photo', 'description')

    def encode(self, photo):
        data = base64.b64encode(photo.read())
        return data

    def create(self, validated_data):
        photo_file = validated_data['photo']
        photo_string = self.encode(photo_file)
        description = validated_data['description']
        token = self.context['token']
        owner = User.objects.filter(id=token).get()

        photo_upload = PhotoUpload.objects.create(photo=photo_string, owner=owner, description=description)

        photo_upload.save()

        return photo_upload


class ReadOnlyPhotoUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoUpload
        fields = ('photo', 'owner', 'description', 'location', 'id')
        read_only_fields = ('photo', 'owner', 'description', 'location', 'id')


class SketchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sketch
        fields = ('img', 'artist', 'sketch_status')

    def encode(self, file):
        data = base64.b64encode(file.read())
        return data

    def create(self, validated_data):
        img_file = validated_data['img']
        img_encoded = self.encode(img_file)
        token = self.context['token']
        owner = User.objects.filter(id=token).get()

        sketch = Sketch.objects.create(img=img_encoded, owner=owner)

        return sketch


class WorkloadSerializer(serializers.HyperlinkedModelSerializer):
    art_permission = serializers.FileField(required=False)

    class Meta:
        model = Workload
        fields = ('photo_upload', 'work_status', 'complete_work', 'generic_status',
                  'art_permission', 'sketches')

    def encode(self, file):
        data = base64.b64encode(file.read())
        return data

    def create(self, validated_data):
        art_permission_encoded = None

        try:
            photo_upload = validated_data['photo_upload']
        except KeyError:
            raise ValidationError

        work_status = validated_data.get('work_status')
        status = validated_data.get('status')

        try:
            art_permission_file = validated_data['art_permission']
            art_permission_encoded = self.encode(art_permission_file)
        except KeyError:
            pass

        workload = Workload.objects.create(photo_upload=photo_upload, work_status=work_status,
                                           art_permission_file=art_permission_encoded, status=status)

        workload.save()

        return workload


class ReadOnlyWorkloadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Workload
        fields = ('photo_upload', 'work_status', 'complete_work', 'generic_status',
                  'art_permission', 'sketches')
        read_only_fields = ('photo_upload', 'work_status', 'complete_work', 'generic_status',
                            'art_permission', 'sketches')


class ArtWorkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArtWork
        fields = ('artist_user', 'photo_after', 'requirements', 'permision_letter_url',
                  'legal_agreement_url', 'sketch')
