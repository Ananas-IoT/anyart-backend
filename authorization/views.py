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


from authorization.serializers import UserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, url_path='login', url_name='login', methods=['get'], permission_classes=[AllowAny])
    def login(self, request):
        try:
            username = request.META['HTTP_USERNAME']
            password = request.META['HTTP_PASSWORD']
        except KeyError:
            return Response({'KeyError': 'Cannot get username or password from headers'},
                            status=status.HTTP_400_BAD_REQUEST)

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
        user_serializer = self.get_serializer(data=request.data)



        user_serializer.is_valid(raise_exception=True)
        try:
            user_serializer.username_exists()
        except serializers.ValidationError:
            return Response("Such username already exists", status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(user_serializer)
        headers = self.get_success_headers(user_serializer.validated_data)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)

        profile_dict = {'first_name': request.data.get('first_name'),
                        'last_name': request.data.get('last_name'),
                        'rights': request.data.get('rights')}
        profile_serializer = UserProfileSerializer(data=profile_dict)
        profile_serializer.is_valid(raise_exception=True)

        self.perform_profile_create(profile_serializer, username=user.username)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, headers=headers, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

    def perform_profile_create(self, serializer, **kwargs):
        instance = serializer.save(**kwargs)
        instance.save()

