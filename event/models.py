from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    win_rate = models.FloatField(null=True, blank=True)
    total_games = models.IntegerField(null=True, blank=True)
    wins = models.IntegerField(null=True, blank=True)
    loses = models.IntegerField(null=True, blank=True)


class Event(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, related_name='event_creator', on_delete=models.CASCADE)
    opponent = models.ForeignKey(User, related_name='event_opponent', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
