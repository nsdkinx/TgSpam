# -*- coding: utf-8 -*-

from dataclasses import dataclass

from account.telegram_account import TelegramAccount
from proxy.model import Proxy


@dataclass
class ParametersVerifyingResult:
    """Stores the accounts and proxies needed for module work
    after processing them at the parameters verifying section."""
    accounts: list[TelegramAccount]


class NeedToExitModule:
    pass


class NeedToEditParameters:
    pass
