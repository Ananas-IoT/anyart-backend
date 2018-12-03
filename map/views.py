from json import dumps, loads

from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from anyart_backend.permissions import IsBasicUserOrArtist, IsTokenAuthenticated
from map.serializers import LocationSerializer, LimitationSerializer, WorkloadSerializer, PhotoUploadSerializer, \
    ReadOnlyPhotoUploadSerializer, ReadOnlyWorkloadSerializer, SketchSerializer, SketchReadOnlySerializer
from map.models import Location, Limitation, Workload, PhotoUpload, Sketch
from geopy.geocoders import Nominatim

import json


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    # permission_classes = (IsTokenAuthenticated, IsBasicUserOrArtist, )

    def list(self, request, *args, **kwargs):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)
        restriction_list = serializer.check_in_api()
        print(restriction_list)
        for restriction in restriction_list:
            serializer = LocationSerializer.add_limitation(serializer, location, json.loads(json.dumps(restriction)))
        if restriction_list.__sizeof__() > 0:
            return Response(restriction_list)
        else:
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = LocationSerializer(data=request.data)
        geolocator = Nominatim()

        if serializer.is_valid():

            self.perform_create(serializer)
            try:
                serializer.validated_data['lat']
            except KeyError:
                serializer.validated_data['lat'] = 0

            if serializer.validated_data['lat'] > 0:
                print(serializer.validated_data)
                location = geolocator.reverse([serializer.validated_data['lat'], serializer.validated_data['lng']])
                print(location.address)
                serializer.validated_data['street_address'] = location.address
                serializer.save()
                return Response({'status': 'location added'})
            else:
                geolocator = Nominatim()
                location = geolocator.geocode([serializer.validated_data['street_address']])
                print(location.address)
                print(location.latitude, location.longitude)
                serializer.validated_data['lat'] = location.latitude
                serializer.validated_data['lng'] = location.longitude
                serializer.save()
            return Response({'status': 'location added'})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(company=self.request.data)

    def destroy(self, request, pk, format=None):
        try:
            instance = self.get_object(pk)
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'status': 'location deleted'})

    def partial_update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def get_limitations(self, request, pk, format=None):
        try:

            instance = self.get_object(pk)
            serializer = LocationSerializer(instance)
            print(serializer.data)
            limitations = serializer.data['restrictions']
            return Response(limitations)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def add_limitation(self, request, pk, format=None):

        try:
            location = self.get_object(pk)
            serializer = LocationSerializer(self)
            restriction = request.data

            serializer = LocationSerializer.add_limitation(serializer,location,restriction)
            return Response(serializer.data, status=HTTP_201_CREATED)

        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)


# location = geolocator.geocode("Лукаша 5 Львів, Львівська область, 79000")
# location = geolocator.reverse("49.821884, 23.987562")
class LimitationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def list(self, request):
        queryset = Limitation.objects.all()
        serializer = LimitationSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Limitation.objects.get(pk=pk)
        except Limitation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        limitation = self.get_object(pk)
        serializer = LimitationSerializer(limitation)
        return Response(serializer.data)

    def destroy(self, request, pk, format=None):
        try:
            instance = self.get_object(pk)
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'status': 'limitation deleted'})

    def create(self, request, *args, **kwargs):
        serializer = LimitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'limitation added'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkloadViewSet(viewsets.ModelViewSet):
    queryset = Workload.objects.all()
    serializer_class = WorkloadSerializer

    def create(self, request, *args, **kwargs):
        serializer = WorkloadSerializer(data=request.data, context={'token': request.auth.user_id})
        if serializer.is_valid():
            workload = self.perform_create(serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        photo_upload_id = PhotoUpload.objects.filter(workload=workload).get().id
        return Response({'photo_upload_id': photo_upload_id}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOnlyWorkloadSerializer
        return WorkloadSerializer


class PhotoUploadViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoUploadSerializer
    queryset = PhotoUpload.objects.all()
    permission_classes = (IsTokenAuthenticated,)

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
    def get_by_id(self, request, pk=None):
        instance = self.get_object()
        serializer = ReadOnlyPhotoUploadSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SketchViewSet(viewsets.ModelViewSet):
    queryset = Sketch.objects.all()
    serializer_class = SketchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data, context={'token': request.auth.user_id})

        if serializer.is_valid():
            self.perform_create(serializer)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('sketch added', status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data, context={'token': request.auth.user_id})

        if serializer.is_valid():
            self.perform_update(serializer)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('sketch updated', status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SketchReadOnlySerializer
        return SketchSerializer
