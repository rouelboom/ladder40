from rest_framework import serializers
from django.conf import settings as django_settings
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer

from event.models import Event, User

# User = django_settings.AUTH_USER_MODEL

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = '__all__'


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'username', 'first_name',
            'last_name', 'email', 'is_subscribed')
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
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }
