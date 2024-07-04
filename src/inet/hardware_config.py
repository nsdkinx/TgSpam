# -*- coding: utf-8 -*-

import platform
from .utils import execute_wmic_command


class HardwareConfig:
    machine = platform.machine()
    csproduct_uuid = execute_wmic_command('wmic csproduct get uuid /value')
    bios_serial = execute_wmic_command('wmic bios get SerialNumber /value')
