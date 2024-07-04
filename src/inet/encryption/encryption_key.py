# -*- coding: utf-8 -*-

import hashlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .encoding import encode_to_base64


def derive_fernet_key_from_string_insecure(secret_key: str) -> bytes:
    key = hashlib.sha256(secret_key.encode()).digest()
    return encode_to_base64(key)


def derive_fernet_key_from_string(secret_key: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    derived = kdf.derive(secret_key.encode('UTF-8'))
    return encode_to_base64(derived)
