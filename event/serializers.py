from rest_framework import serializers
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer

from event.models import Event, User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'username', 'first_name',
            'last_name', 'email', 'win_rate')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            'password', 'last_name', 'first_name', 'username'
        )
        extra_kwargs = {
            # 'first_name': {'required': True},
            # 'last_name': {'required': True},
            # 'email': {'required': True},
        }


class EventSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'author', 'creation_date', 'event_date', 'title')

    def update(self, instance, validated_data):
        instance.opponent = validated_data.pop('opponent')
        return super().update(instance, validated_data)
