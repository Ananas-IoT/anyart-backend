from django.shortcuts import render
from django.contrib.auth import views
# Create your views here.
from rest_framework import viewsets, filters, generics
from  rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from authorization.serializers import UserSerializer
from upload.models import Sketch


class SketchViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Sketch.objects.all()
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, filters.BaseFilterBackend)



class CreateUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

