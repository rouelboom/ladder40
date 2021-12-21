from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response


from event.serializers import EventSerializer, CustomUserSerializer

from event.models import Event, User


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-event_date')
    serializer_class = EventSerializer

    @action(methods=['post', 'put'], detail=True,
            permission_classes=[IsAuthenticated]
            )
    def subscribe(self, request, pk=None):
        event = get_object_or_404(klass=Event, id=pk)
        print(request.user)
        if request.user == event.author:
            return Response({'error': 'You can`t subscribe to yourself event!'})
        else:
            if event.opponent is not None:
                return Response({'error': 'Opponent for event already founded'})
            # event.opponent = request.user
            # event.save()
            data = {
                'title': event.title,
                'opponent': request.user
            }
            serializer = self.get_serializer(
                data=data, context={'request': request, 'event': event})
            serializer.is_valid(raise_exception=True)
            print(serializer.data)
            # serializer.update()
            # send notification to creator
            return Response('PI BA LA PU KA!')

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated]
            )
    def unsubscribe(self, request, pk=None):
        event = get_object_or_404(klass=Event, id=pk)
        print(request.user)
        if request.user != event.opponent:
            return Response({'error': 'You should subscribe to event before unsubscribe from this!'})
        event.opponent = None
        event.save()
        # send notification to creator
        return Response('PI BA LA PU KA!')


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    # permission_classes = IsAuthenticatedOrReadOnly

