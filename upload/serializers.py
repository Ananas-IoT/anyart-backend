from rest_framework import serializers

from upload.models import PhotoUpload, Sketch, Workload, ArtWork


class PhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoUpload
        fields = ('photo_url', 'location', 'user')


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
