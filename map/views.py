
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from anyart_backend.permissions import IsBasicUserOrArtist, IsTokenAuthenticated
from map.serializers import LocationSerializer, LimitationSerializer
from map.models import Location
from geopy.geocoders import Nominatim

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    permission_classes = (IsTokenAuthenticated, IsBasicUserOrArtist, )

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
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        serializer = LocationSerializer(data=request.data)
        geolocator = Nominatim()

        if serializer.is_valid():
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
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

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

    def add_limitations(self, request, pk, format=None):

        try:
            instance = self.get_object(pk)
            print(instance)

            serializer = LocationSerializer(instance, data=request.data)
            limitations = LimitationSerializer(data=request.data)
            # print(limitations.initial_data)
            # print(repr(limitations))
            if limitations.is_valid() and serializer.is_valid():
                limitations.save()
                print(limitations.data)
                serializer.validated_data['restrictions'] = []
                serializer.validated_data['restrictions'].append(limitations.data)
                serializer.perform_update()
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)
# location = geolocator.geocode("Лукаша 5 Львів, Львівська область, 79000")
# location = geolocator.reverse("49.821884, 23.987562")
