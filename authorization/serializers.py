from rest_framework import serializers

from approval.models import Veto
from authorization.models import *


class UserGroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, blank=False, default='')
    users = User(many=True)

    def create(self, validated_data):
        return UserGroup.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.users = validated_data.get('users', instance.user)
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(unique=True)
    password = serializers.CharField(max_length=100, blank=False, default='')
    role = serializers.CharField(max_length=100, blank=True, default='')
    user_profile = UserProfile(many=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, blank=False, default='')
    last_name = serializers.CharField(max_length=100, blank=False, default='')
    nickname = serializers.CharField(max_length=100, blank=True, default='')
    user_login = serializers.CharField(max_length=100, blank=True, default='')

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('role', instance.role)
        instance.nickname = validated_data.get('name', instance.nickname)
        instance.user_login = validated_data.get('user_login', instance.user_login)
        instance.save()
        return instance


class UserHierarchyWrapperSerializer(serializers.Serializer):
    user = User()
    hierarchy_rank = serializers.IntegerField(default=1)
    veto_list = Veto(many=True)

    def create(self, validated_data):
        return UserHierarchyWrapper.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.hierarchy_rank = validated_data.get('hierarchy_rank', instance.hierarchy_rank)
        instance.veto_list = validated_data.get('veto_list', instance.veto_list)
        instance.save()
        return instance


class HierarchySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, blank=False, default='')
    users = UserHierarchyWrapper(many=True)

    def create(self, validated_data):
        return HierarchySerializer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.users = validated_data.get('users', instance.users)
        instance.save()
        return instance
