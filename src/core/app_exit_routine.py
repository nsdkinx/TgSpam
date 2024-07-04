# -*- coding: utf-8 -*-

import asyncio
import sys
import time

from .connected_accounts_manager import ConnectedAccountsManager


class AppExitRoutine:
    """Handles application exit.
    Disconnects connecting clients, disconnects INET WebSocket,
    etc"""

    @staticmethod
    async def exit_app():
        await ConnectedAccountsManager.disconnect_all_accounts()
        return

    @classmethod
    def exit_app_sync(cls):
        task = asyncio.create_task(cls.exit_app())
        time.sleep(0.3)
        return sys.exit(0)
