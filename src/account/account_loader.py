# -*- coding: utf-8 -*-

from __future__ import annotations

import logging

from pathlib import Path
from typing import Generator

from telethon.sessions.sqlite import SQLiteSession

from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _
from core.utils.mixins.shared_instance_mixin import SharedInstanceMixin
from proxy.proxy_manager import ProxyManager
from .json_file import JsonFile
from .telegram_account import TelegramAccount

logger = logging.getLogger(__name__)


class AccountLoader(SharedInstanceMixin):
    """Find .session files in a given folder, loads proxies and makes
    TelegramAccount objects.
    Pretty high level so interacting with console is allowed"""

    def __init__(self, account_folder: Path):
        self.account_folder = account_folder
        self._proxy_manager = ProxyManager.get_shared()
        self._accounts: list[TelegramAccount] = []

        super().__init__()

    def iter_session_files(self) -> Generator[Path, None, None]:
        return self.account_folder.glob('*.session')

    @property
    def total_accounts(self) -> int:
        return len(self.get_accounts())

    def _load_accounts(self):
        logger.info('Starting to load accounts...')
        if self._accounts:
            logger.info(f'We already have {len(self._accounts)} loaded. Clearing the list')
            self._accounts.clear()
        for session_file in self.iter_session_files():
            logger.info(f'[{session_file}] Starting to load...')
            try:
                corresponding_json_file = session_file.with_suffix('.json')
                if not corresponding_json_file.exists():
                    logger.info(f'[{session_file}] JSON file not found. Skipping.')
                    ui.log('[red]' + _("ACCOUNT-json_not_found").format(session_file) + '[/red]')
                    continue

                corresponding_json_file = JsonFile(corresponding_json_file)
                logger.info(f'[{session_file}] Found {corresponding_json_file}')
                api_data = corresponding_json_file.extract_api_data()
                logger.info(f'[{session_file}] Extracted API data. API pair: {api_data.api_id}:{api_data.api_hash}')
                account_info = corresponding_json_file.get_account_info(api_data)
                logger.info(f'[{session_file}] Got account information => {account_info}')
                proxy = self._proxy_manager.get_proxy_for_session_file(session_file)
                logger.info(f'[{session_file}] Got proxy => {proxy}')
                account = TelegramAccount(
                    session=SQLiteSession(str(session_file)),
                    api_data=api_data,
                    account_info=account_info,
                    proxy=proxy
                )
                logger.info(f'[{session_file}] Loaded successfully!')
                self._accounts.append(account)
            except BaseException as e:
                logger.exception(f'[{session_file}] Exception while loading account.')
                exc = f'{type(e).__name__}: {str(e)}'
                ui.log('[red]' + _("ACCOUNT-error_loading_account").format(str(session_file), exc) + '[/red]')
                continue

        logger.info(f'Successfully loaded {len(self._accounts)} accounts!')
        return

    def get_accounts(self) -> list[TelegramAccount]:
        self._load_accounts()
        return self._accounts
