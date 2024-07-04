# -*- coding: utf-8 -*-

import logging

from .license import License
from .errors import *
from .encrypted_client import EncryptedClient

from datetime import datetime

logger = logging.getLogger(__name__)


class Authorizer:
    """Controls program access and activated modules"""
    license: License = None

    def __init__(self, encrypted_client: EncryptedClient):
        self.encrypted_client = encrypted_client

    async def authorize(self, license_key: str, hwid: str) -> License:
        result = await self.encrypted_client.client_gateway(license_key, hwid)
        if result == 403:
            logger.error(f'result.status = 403, raising UsedOnOtherDeviceError')
            raise UsedOnOtherDeviceError
        elif result == 404:
            logger.error(f'result.status = 404, raising KeyNotFoundError')
            raise KeyNotFoundError
        elif isinstance(result, int) and result != 200:
            logger.error(f'result = {result}')
            raise UnableToConnectError

        expiry_date = datetime.fromtimestamp(result['expiry_date'])
        expiry_days = (expiry_date - datetime.now()).days + 1
        if expiry_days <= 0:
            logger.error(f'expiry_days = {expiry_days}, raising LicenseExpiredError')
            raise LicenseExpiredError

        self.__class__.license = License(license_key, result['modules'], expiry_days)
        return self.__class__.license
