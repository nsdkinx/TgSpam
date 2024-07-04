# -*- coding: utf-8 -*-

import os


def generate_random_salt(length: int = 16) -> bytes:
    return os.urandom(length)
