from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    win_rate = models.FloatField(null=True, blank=True)
    total_games = models.IntegerField(null=True, blank=True)
    wins = models.IntegerField(null=True, blank=True)
    loses = models.IntegerField(null=True, blank=True)


class Event(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, related_name='event_creator', on_delete=models.CASCADE,
                               null=True, blank=True)
    opponent = models.ForeignKey(User, related_name='event_opponent', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Author {self.author.username}, event: {self.title}'


class TelegramUserToPasswordRelation(models.Model):
    user_id = models.IntegerField() # telegram user id
    password = models.CharField(max_length=150)
    # изначально при логине через телеграм login=username (а может быть даже login=user_id),
    # позже после входа через сайт пользователь сможет создать новый логин пароль
    username = models.CharField(max_length=150)
    token = models.CharField(max_length=150, null=True, blank=True)
    site_access = models.BooleanField(default=False)
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'user_id {self.user_id}'
