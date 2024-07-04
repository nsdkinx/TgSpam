# -*- coding: utf -*-

from cryptography.fernet import Fernet
from .encoding import encode_to_base64, decode_from_base64
from .encryption_key import derive_fernet_key_from_string
from .salt import generate_random_salt


class StringCryptor:

    def __init__(self, encryption_key: str) -> None:
        self.encryption_key = encryption_key

    def encrypt(self, data: str) -> str:
        salt = generate_random_salt()
        key = derive_fernet_key_from_string(self.encryption_key, salt)
        f = Fernet(key)
        return encode_to_base64(
            salt + f.encrypt(data.encode("utf-8")),
            decode_on_return=True
        )

    def decrypt(self, data: str) -> str:
        encrypted_data_bytes = decode_from_base64(data)
        salt = encrypted_data_bytes[:16]
        key = derive_fernet_key_from_string(self.encryption_key, salt)
        f = Fernet(key)
        return f.decrypt(encrypted_data_bytes[16:]).decode("utf-8")
