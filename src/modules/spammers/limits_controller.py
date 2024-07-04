# -*- coding: utf-8 -*-

from account.telegram_account import TelegramAccount
from .errors import AccountLimitHitError, OverallLimitHitError


class LimitsController:
    """Controls that accounts do not go beyond
    the set limits"""

    def __init__(self, overall_limit: int, account_limit: int):
        self.overall_limit = overall_limit
        self.account_limit = account_limit
        self._total_sends = 0
        self._account_sends_table: dict[str, int] = {}

    def _increment_sends_for_account(self, account: TelegramAccount):
        _name = account.account_info.session_name
        self._total_sends += 1
        if _name not in self._account_sends_table:
            self._account_sends_table[_name] = 1
        else:
            self._account_sends_table[_name] += 1

    def record_send(self, account: TelegramAccount):
        _name = account.account_info.session_name
        self._increment_sends_for_account(account)
        if self._total_sends >= self.overall_limit:
            raise OverallLimitHitError
        if self._account_sends_table[_name] >= self.account_limit:
            raise AccountLimitHitError

        return

    def is_overall_limit_hit(self):
        return self._total_sends >= self.overall_limit

    def get_account_sends_table(self):
        return self._account_sends_table
