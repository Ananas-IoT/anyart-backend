from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="auth:user-detail")
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
        model = User
        fields = ('url', 'id', 'username', 'password', 'sketches', 'snippets', 'email', 'first_name', 'last_name', 'last_login')

    def username_exists(self):
        username = self.validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('username already exists')
