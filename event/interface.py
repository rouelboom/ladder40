import os
from datetime import datetime
import logging

import pytz
import requests
from rest_framework import status
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from event import const
from event.models import Event, TelegramUserToPasswordRelation


load_dotenv()


ENCRYPT_KEY = os.getenv('ENCRYPT_KEY')

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
    print('123')
    encrypted_default_password = encrypt(str(user_id))
    current_user = TelegramUserToPasswordRelation.objects.filter(user_id=user_id)
    # current_user = TelegramUserToPasswordRelation.objects.all()
    print(current_user.username)

    if not current_user:
        # создать пользователя через djoser
        # залогиниться
        # записать его в TelegramUserToPasswordRelation
        response = requests.post(const.REGISTER_NEW_USER_URL, data={'username': str(user_id),
                                                                    'password': encrypted_default_password})
        print(response.status_code)
        if response.status_code != status.HTTP_201_CREATED:
            logging.debug('WUT???')
            return 'error'
        response = requests.post(const.LOGIN_URL, data={'username': str(user_id),
                                                        'password': encrypted_default_password})
        token = response.json().get('auth_token')
        if token is not None:
            TelegramUserToPasswordRelation.objects.create(user_id=user_id, password=encrypted_default_password,
                                                          username=str(user_id), token=encrypt(token),
                                                          last_update=datetime.now(tz=pytz.UTC).isoformat())
        else:
            return 'error'
    print(current_user.token)


def encrypt(message_to_encrypt: str) -> str:
    """
    Encrypts message by sync key
    :param message_to_encrypt:
    :return: encrypted message
    """
    crypto = Fernet(ENCRYPT_KEY.encode())
    encrypted_message = crypto.encrypt(message_to_encrypt.encode())
    return encrypted_message.decode()


def decrypt(message_to_decrypt):
    """
    Decrypt message by sync key
    :param message_to_decrypt:
    :return: decrypted message
    """
    decrypto = Fernet(ENCRYPT_KEY.encode())
    decrypted_message = decrypto.decrypt(message_to_decrypt.encode())
    return decrypted_message.decode()