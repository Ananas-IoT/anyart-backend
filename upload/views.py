from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from anyart_backend.permissions import IsTokenAuthenticated
from upload.models import Sketch, PhotoUpload
from upload.serializers import SketchSerializer, PhotoUploadSerializer, ReadOnlyPhotoUploadSerializer


class SketchViewSet(viewsets.ModelViewSet):
    serializer_class = SketchSerializer
    permission_classes = (IsTokenAuthenticated, )
    queryset = Sketch.objects.all()
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, filters.BaseFilterBackend)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({})


class PhotoUploadViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = PhotoUploadSerializer
    queryset = PhotoUpload.objects.all()
    permission_classes = (IsTokenAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = PhotoUploadSerializer(data=request.data, context={'token': request.auth.user_id})

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response("Invalid data in serializer")

        self.perform_create(serializer)

        return Response({'image': 'created'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def get_all(self, request):
        serializer = ReadOnlyPhotoUploadSerializer(self.queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def get_by_id(self, request, id=None):
        instance = self.get_object()
        serializer = ReadOnlyPhotoUploadSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
