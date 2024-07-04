# -*- coding: utf-8 -*-

import asyncio
import sqlite3
import logging
from typing import Optional

from opentele.tl import TelegramClient
from opentele.api import APIData
from python_socks import ProxyTimeoutError
from telethon.sessions import Session
from telethon.tl.types import User

from .account_info import AccountInfo
from proxy.model import Proxy
from proxy.json_proxy_manager import JsonProxyManager
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _
from core.filesystem.container import files

from pathlib import Path

logger = logging.getLogger(__name__)


class TelegramAccount(TelegramClient):
    """Custom version of opentele.tl.TelegramClient that has
    account, session name and phone as arguments for easy access.
    Also using the Proxy model instead of dict (made kind of ugly for now,
    but nobody cares lol).
    :param api_data: Subclass of opentele.api.APIData with neccessary api params.
    Get them from JSON."""

    def __init__(
        self,
        session: Session,
        api_data: APIData,
        account_info: AccountInfo,
        proxy: Proxy = None
    ):
        super().__init__(
            session=session,
            api=api_data,
            proxy=proxy.telethon if proxy else None
        )
        self.api_data = api_data
        self.account_info = account_info
        self.proxy = proxy
        self._account_lock = asyncio.Lock()

    def __repr__(self):
        return self.account_info.session_name

    async def acquire_lock(self):
        if self._account_lock.locked():
            ui.log(_("ACCOUNT-lock_is_acquired").format(self.account_info.session_name))
            await self._account_lock.acquire()
            ui.log(_("ACCOUNT-lock_is_released").format(self.account_info.session_name))
        else:
            return await self._account_lock.acquire()

    async def release_lock(self):
        return self._account_lock.release()

    def change_proxy(self, new_proxy: Proxy, write_to_json: bool = True):
        if write_to_json:
            JsonProxyManager.write_proxy_into_json_file(
                self.account_info.session_file.with_suffix('.json'),
                new_proxy
            )
        self.proxy = new_proxy
        logger.info(f'[{self.account_info.session_file}] Changed proxy to {new_proxy}')
        return

    async def connect_and_check(self) -> Optional[User]:
        """Connects to the account, checks it for validity
        and returns its' User object (or None if the account
        is dead)"""
        try:
            await self.connect()
            _me = await self.get_me()
            _me.first_name # noqa
            return _me
        except sqlite3.OperationalError:
            ui.print('[red]' + _('ACCOUNT-database_locked').format(self.account_info.session_name) + '[/red]')
            # await self.disconnect()
            return False
        except ProxyTimeoutError:
            ui.print('[red]' + _("PROXY-timeout") + '[/red]')
            return False
        except BaseException as e:
            ui.print('[red]' + _("MODULE-base-account_is_dead").format(self) + '[/red]')
            await self.disconnect()
            # await self.move_to_folder(files.dead_accounts_folder)
            return False

    async def move_to_folder(self, folder: Path):
        """Moves the session and json file to the given folder.
        Disconnects the account if it's connected."""
        if self.is_connected():
            try:
                await self.disconnect()
            except sqlite3.OperationalError:
                pass

        from core.settings.container import settings
        if not settings.sort_accounts_to_folders:
            return

        try:
            self.account_info.session_file.rename(folder / self.account_info.session_file.name)
            json_file = self.account_info.session_file.with_suffix('.json')
            if json_file.exists():
                json_file.rename(folder / json_file.name)

            logger.info(f'Moved account {self.account_info.session_file} into {folder}')
        except FileExistsError:
            pass
        except PermissionError:
            await self.disconnect()
            await self.move_to_folder(folder)
        except BaseException:
            logger.exception(f'Error while moving {self.account_info.session_name} to {folder}')
            pass
        return
