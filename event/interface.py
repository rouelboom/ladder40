import logging
import requests
from rest_framework import status

from event import const
from event.models import Event, TelegramUserToPasswordRelation

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
    default_password = str(user_id) + 'QWE123'
    current_user = TelegramUserToPasswordRelation.objects.filter(user_id=user_id)
    if not current_user:
        # создать пользователя через djoser
        # записать его в TelegramUserToPasswordRelation
        # залогиниться
        response = requests.post(const.REGISTER_NEW_USER_URL, data={'username':str(user_id),
                                                                    'password': default_password})
        if response.status_code != status.HTTP_200_OK:
            logging.debug('WUT???')
            return 'error'



