# -*- coding: utf-8 -*-

import json
from typing import Union
import aiohttp

from .encryption.string_cryptor import StringCryptor
from .config import encryption_key

from core.release_info import application_version

cryptor = StringCryptor(encryption_key)


class EncryptedSession:
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._headers = {'User-Agent': f'SMM-SOFT/{application_version}'}

    async def send_get_request(self, request: str, data: dict) -> Union[dict, int]:
        token = cryptor.encrypt(json.dumps(data))
        async with aiohttp.ClientSession(self._base_url, headers=self._headers) as session:
            response = await session.get(request + f'?token={token}')
            text = await response.text(encoding='utf-8')
            if '[' in text and '{' in text:
                return json.loads(text)
            try:
                text = cryptor.decrypt(text)
                return json.loads(text)
            except:
                return response.status

    async def send_post_request(self, request: str, data: dict):
        token = cryptor.encrypt(json.dumps(data))
        async with aiohttp.ClientSession(self._base_url, headers=self._headers) as session:
            response = await session.post(request + f'?token={token}')
            text = await response.text(encoding='utf-8')
            if '[' in text and '{' in text:
                return json.loads(text)
            try:
                text = cryptor.decrypt(text)
                return json.loads(text)
            except:
                return response.status
