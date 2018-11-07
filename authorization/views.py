from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import views, get_user_model, authenticate
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, status, serializers
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from authorization.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, url_path='login', url_name='login', methods=['get'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    @permission_classes((AllowAny,))
    def create(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.username_exists()
        except serializers.ValidationError:
            return Response("Such username already exists", status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.validated_data)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, headers=headers, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

