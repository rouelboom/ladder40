
from datetime import datetime
import logging

import pytz
import requests
from rest_framework import status
from django.db.models import Model

from event import const
from event.models import Event, TelegramUserToPasswordRelation
from event.utils import decrypt, encrypt
from event.exceptions import LoginError


logging.basicConfig(filename='logger40.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


def _login(username, password):
    """

    :return token
    """
    print(username, '------' , password)
    response = requests.post(const.LOGIN_URL, data={'username': username,
                                                    'password': password})
    print(response.json())
    if response.status_code != status.HTTP_200_OK:
        return {'error': {'login': f'status code {response.status_code}'}}
    token = response.json().get('auth_token')
    if token is None:
        return {'error': {'login': 'no token in response'}}

    return token


def _update_token_in_relative_table(user_id, token):
    """
    Update token for user in TelegramUserToPasswordRelation
    :param user_id:
    :param token:
    :return:
    """
    try:
        token = encrypt(token)
        # relation = TelegramUserToPasswordRelation.objects.get(user_id=user_id)
        relation = TelegramUserToPasswordRelation.objects.filter(user_id=user_id)
        relation = relation.values()[0]
        relation.token = token
        relation.save(update_fields=['token'])
    except TelegramUserToPasswordRelation.DoesNotExist:
        return {'error': 'TelegramUserToPasswordRelation object does not exist'}
    except TelegramUserToPasswordRelation.MultipleObjectsReturned:
        return {'error': 'TelegramUserToPasswordRelation multiple object returned'}


def _get_password_proxy(password) -> str:
    """

    :param password:
    :return:
    """
    proxy_password = ''
    for letter in password:
        proxy_password += f'{letter}1'
    return proxy_password


def _create_user(username, password):
    """

    :param username:
    :param password:
    :return:
    """
    response = requests.post(const.REGISTER_NEW_USER_URL, data={'username': username,
                                                                'password': password})
    if response.status_code != status.HTTP_201_CREATED:
        return {'error': 'error while creating new user'}


def authenticate(user_id: dict) -> str:
    """
    Login to API
    Args:
        user_id: telegram_id of user
    Returns:
        token
    """
    username = str(user_id)
    encrypted_default_password = encrypt(username)
    proxy_password = _get_password_proxy(username)
    current_user = TelegramUserToPasswordRelation.objects.filter(user_id=user_id)

    if not current_user:
        # создать пользователя через djoser
        # залогиниться
        # записать его в TelegramUserToPasswordRelation
        _create_user(username, encrypted_default_password)
        token = _login(username, encrypted_default_password)
        if token.get('error'):
            return 'error'
        # TODO нужно сгенерировать пароль, зашифровать его и записать в базу
        # перед логином получать из базы и дешифровать
        token = encrypt(token)
        TelegramUserToPasswordRelation.objects.create(user_id=user_id, password=encrypted_default_password,
                                                      username=username, token=token,
                                                      last_update=datetime.now(tz=pytz.UTC).isoformat())
        return token

    token = _login(username, encrypted_default_password)
    if token.get('error'):
        return 'error'
    print('4')
    result = _update_token_in_relative_table(user_id, token)
    print('5')
    if result.get('error'):
        return 'error'
    return token

