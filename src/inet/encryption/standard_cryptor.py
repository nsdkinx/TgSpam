# -*- coding: utf -*-

from cryptography.fernet import Fernet
from .encoding import encode_to_base64, decode_from_base64
from .encryption_key import derive_fernet_key_from_string
from .salt import generate_random_salt


class StandardCryptor:

    def __init__(self, encryption_key: str) -> None:
        self.encryption_key = encryption_key

    def encrypt(self, data: bytes) -> bytes:
        salt = generate_random_salt()
        key = derive_fernet_key_from_string(self.encryption_key, salt)
        f = Fernet(key)
        return salt + f.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        salt = data[:16]
        key = derive_fernet_key_from_string(self.encryption_key, salt)
        f = Fernet(key)
        return f.decrypt(data[16:])
