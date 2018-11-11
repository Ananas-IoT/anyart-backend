from django.shortcuts import render
from django.contrib.auth import views
# Create your views here.
from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


from authorization.serializers import UserSerializer
from upload.models import Sketch, PhotoUpload
from upload.serializers import SketchSerializer, PhotoUploadSerializer


class SketchViewSet(viewsets.ModelViewSet):
    serializer_class = SketchSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Sketch.objects.all()
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, filters.BaseFilterBackend)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({})


class PhotoUploadViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoUploadSerializer
    queryset = PhotoUpload.objects.all()








