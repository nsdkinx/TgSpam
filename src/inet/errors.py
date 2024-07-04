# -*- coding: utf-8 -*-

from core.localization.interface import _


class InetError(Exception):
    pass


class KeyNotFoundError(InetError):
    def __init__(self):
        super().__init__(_("INET-key_not_found"))


class UsedOnOtherDeviceError(InetError):
    def __init__(self):
        super().__init__(_("INET-used_on_other_device"))


class UnableToConnectError(InetError):
    def __init__(self):
        super().__init__(_("INET-unable_to_connect"))


class LicenseExpiredError(InetError):
    def __init__(self):
        super().__init__(_("INET-license_expired"))
