# -*- coding: utf-8 -*-

import logging
from inet.software_config import SoftwareConfig
from inet.hardware_config import HardwareConfig

logger = logging.getLogger(__name__)


def log_computer_info() -> None:
    logger.info('SOFTWARE CONFIGURATION:')
    logger.info(f'    1. OS: {SoftwareConfig.os_with_version}')
    logger.info(f'    2. Python: {SoftwareConfig.python_version}')
    logger.info(f'    3. Telethon: {SoftwareConfig.telethon}')
    logger.info('HARDWARE CONFIGURATION:')
    logger.info(f'    1. System UUID: {HardwareConfig.csproduct_uuid}')
    logger.info(f'    2. BIOS serial: {HardwareConfig.bios_serial}')
    return
