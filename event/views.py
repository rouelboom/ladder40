from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from event.serializers import EventSerializer, CustomUserSerializer

from event.models import Event, User


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-event_date')
    serializer_class = EventSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
