from rest_framework import serializers

from upload.models import PhotoUpload, Sketch, Workload, ArtWork
from django.core.files import File
import base64


class PhotoUploadSerializer(serializers.ModelSerializer):
    # photo = serializers.SerializerMethodField()

    class Meta:
        model = PhotoUpload
        fields = ('photo', )

    # def get_photo(self, obj):
    #     f = open(obj.photo.path, 'rb')
    #     image = File(f)
    #     data = base64.b64encode(image.read())
    #     f.close()
    #     return data


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
