# -*- coding: utf-8 -*-

import platform
from telethon.version import __version__ as telethon_version


class SoftwareConfig:
    python_version = platform.python_version()
    telethon = telethon_version
    os_with_version = platform.system() + ' ' + platform.release()
