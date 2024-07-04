# -*- coding: utf-8 -*-

import aiohttp

from .encrypted_session import EncryptedSession


class EncryptedClient:
    """Low-level interface for interacting with the inet http api (encrypted)"""

    def __init__(self, base_url: str):
        self._base_url = base_url
        self._encrypted_session = EncryptedSession(base_url)

    async def client_gateway(self, license_key: str, hwid: str) -> dict:
        data = {
            'license_key': license_key,
            'hwid': hwid
        }
        return await self._encrypted_session.send_get_request('/user/client_gateway', data=data)

    async def telemetry(self, message: str):
        data = {
            'message': message
        }
        return await self._encrypted_session.send_post_request('/user/telemetry', data=data)
