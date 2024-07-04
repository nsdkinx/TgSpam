# -*- coding: utf-8 -*-

import gc
from account.telegram_account import TelegramAccount


class ConnectedAccountsManager:
    """Finds all connected TelegramAccount's and can disconnect them"""

    @staticmethod
    def _iter_all_connected_accounts():
        all_objects = gc.get_objects()
        for obj in all_objects:
            if isinstance(obj, TelegramAccount) and obj.is_connected():
                yield obj

    @classmethod
    async def disconnect_all_accounts(cls):
        """Disconnects all alive account instances"""
        for account in cls._iter_all_connected_accounts():
            await account.disconnect()

        return
