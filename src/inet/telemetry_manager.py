# -*- coding: utf-8 -*-
import asyncio
import logging
from datetime import datetime
from .encrypted_client import EncryptedClient
from .hardware_config import HardwareConfig
from .software_config import SoftwareConfig
from core.utils.mixins.shared_instance_mixin import SharedInstanceMixin
from core.release_info import application_name, application_version

logger = logging.getLogger(__name__)


class TelemetryManager(SharedInstanceMixin):
    """Sends telemetry messages"""

    def __init__(self, encrypted_client: EncryptedClient):
        self._encrypted_client = encrypted_client
        from .authorizer import Authorizer
        self._license = Authorizer.license
        # XXX HACK to init license correctly
        super().__init__()

    async def send_telemetry_message(self, module: str, message: str):
        """This method prepends license info to the original message"""
        current_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S') + f' ({int(datetime.now().timestamp())})'
        formatted_message = f"""- {current_date} -
Новое сообщение телеметрии:
Лицензионный ключ - {self._license.license_key}
Активированные модули - {self._license.activated_modules}
Истекает через - {self._license.expiry_days} дней

HWID - {HardwareConfig.bios_serial}
CSProduct UUID - {HardwareConfig.csproduct_uuid}
ОС - {SoftwareConfig.os_with_version}
Версия софта - {application_name} {application_version}
Модуль - {module}
Сообщение - {message}"""
        try:
            await self._encrypted_client.telemetry(formatted_message)
            logger.info(f'Did send telemetry message (module: {module}, message: {message})')
        except BaseException:
            logger.exception(f'Unable to send telemetry message (module: {module}, message: {message})')

        return
