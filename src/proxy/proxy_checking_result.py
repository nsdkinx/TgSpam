# -*- coding: utf-8 -*-

from enum import Enum
from core.localization.interface import _


class ProxyCheckingResult(str, Enum):
    ALIVE = _("PROXY-alive")
    DEAD = _("PROXY-dead")
    INVALID_CREDENTIALS = _("PROXY-invalid_credentials")
