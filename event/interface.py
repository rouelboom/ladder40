
from datetime import datetime
import logging

import pytz
import requests
from rest_framework import status

from event import const
from event.models import Event, TelegramUserToPasswordRelation
from event.utils import decrypt, encrypt


logging.basicConfig(filename='logger40.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')


def login(user_id: dict) -> str:
    """
    Login to API
    Args:
        user_id: telegram_id of user
    Returns:
        token
    """
    encrypted_default_password = encrypt(str(user_id))
    current_user = TelegramUserToPasswordRelation.objects.filter(user_id=user_id)

    if not current_user:
        # создать пользователя через djoser
        # залогиниться
        # записать его в TelegramUserToPasswordRelation
        response = requests.post(const.REGISTER_NEW_USER_URL, data={'username': str(user_id),
                                                                    'password': encrypted_default_password})
        print(response.status_code)
        if response.status_code != status.HTTP_201_CREATED:
            return 'error'
        response = requests.post(const.LOGIN_URL, data={'username': str(user_id),
                                                        'password': encrypted_default_password})
        token = response.json().get('auth_token')

        if token is not None:
            token = encrypt(token)
            TelegramUserToPasswordRelation.objects.create(user_id=user_id, password=encrypted_default_password,
                                                          username=str(user_id), token=token,
                                                          last_update=datetime.now(tz=pytz.UTC).isoformat())
            return token
        else:
            return 'error'

    return current_user.values()[0].get('token')
