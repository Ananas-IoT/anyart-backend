from django.contrib.auth.models import User
from rest_framework import serializers

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


class ReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoUpload
        fields = ('photo', 'owner', 'description', 'location', 'id')
        read_only_fields = ('photo', 'owner', 'description', 'location', 'id')


class SketchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sketch
        fields = ('img_url', 'restrictions', 'artists', 'sketchStatus')


class WorkloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workload
        fields = ('photo_upload', 'frontend_status', 'complete_work', 'status',
                  'art_permission', 'sketches')


class ArtWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtWork
        fields = ('artist_user', 'photo_after', 'requirements', 'permision_letter_url',
                  'legal_agreement_url', 'sketch')
