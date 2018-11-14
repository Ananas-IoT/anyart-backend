from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from authorization.models import UserProfile


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    rights = serializers.CharField(required=True)
    owner = serializers.ReadOnlyField(source='owner.username', required=False)
    sketches = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='sketch-detail',
        read_only=True,
    )
    snippets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='snippet-detail',
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = ('url', 'id', 'owner', 'first_name', 'last_name', 'rights',
                  'snippets', 'sketches')

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        rights = validated_data['rights']
        username = validated_data['username']

        owner = User.objects.filter(username=username).get()

        user_profile = UserProfile.objects.create(first_name=first_name, last_name=last_name,
                                                  owner=owner, rights=rights)

        user_profile.save()
        return user_profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="auth:user-detail")

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password',
                  'email', 'last_login', 'first_name', 'last_name')

    def username_exists(self):
        username = self.validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('username already exists')
