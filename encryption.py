""" Provides encryption and decryption functions for securely storing passwords. """


import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets


def encrypt_password(key, password):
    """ Encrypt the password and return nonce & ciphertext. """
    nonce = secrets.token_bytes(12)
    password = password.encode()
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, password, None)

    # Change the nonce and ciphertext into a readable Base64 string 
    nonce = base64.b64encode(nonce).decode()
    ciphertext = base64.b64encode(ciphertext).decode()
    return nonce, ciphertext


def decrypt_password(key, nonce, ciphertext):
    """ Decrypt the password stored in the passwords.json. """
    nonce = base64.b64decode(nonce)
    ciphertext = base64.b64decode(ciphertext)
    aesgcm = AESGCM(key)
    password = aesgcm.decrypt(nonce, ciphertext, None)

    return password.decode()