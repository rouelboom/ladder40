from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from event.models import Event, User
from event.views import EventViewSet, CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename='events')
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = router.urls
# urlpatterns = [
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]