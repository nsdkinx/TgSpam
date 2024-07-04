# -*- coding: utf-8 -*-

import base64
from typing import Union


def encode_to_base64(data: Union[str, bytes], decode_on_return: bool = False) -> Union[str, bytes]:
    if isinstance(data, str):
        data = data.encode('UTF-8')

    encoded = base64.urlsafe_b64encode(data)
    if decode_on_return:
        return encoded.decode('UTF-8')
    else:
        return encoded


def decode_from_base64(data: Union[str, bytes], decode_on_return: bool = False) -> Union[str, bytes]:
    decoded = base64.urlsafe_b64decode(data)

    if decode_on_return:
        return decoded.decode('UTF-8')
    else:
        return decoded
