import os
import secrets
import string
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

ENCRYPT_KEY = os.getenv('ENCRYPT_KEY')


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


def _generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password
