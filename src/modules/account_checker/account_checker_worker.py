# -*- coding: utf-8 -*-

import logging
import asyncio
import sqlite3
import traceback
from typing import Optional

from core.localization.interface import _
from core.ui.ui_manager import UIManager as ui
from account.telegram_account import TelegramAccount
from .account_checker_parameters import AccountCheckerParameters
from .account_checking_result import AccountCheckingResult
from .spamblock_checker import SpamblockChecker
from .spamblock_checking_result import SpamblockCheckingResult
from core.filesystem.container import files

from telethon.errors import rpcerrorlist as errors

logger = logging.getLogger(__name__)


class AccountCheckerWorker:
    """Coordinates a single account."""

    def __init__(
            self,
            account: TelegramAccount,
            parameters: AccountCheckerParameters
    ):
        self.account = account
        self.parameters = parameters

    def _log(self, text: str, color: Optional[str] = None):
        if color:
            return ui.log(f'[{color}]({_("account")} {self.account.account_info.session_name}) {text}[/{color}]')
        return ui.log(f'({_("account")} {self.account.account_info.session_name}) {text}')

    async def start_working(self):
        self._log(_('MODULE-base-connecting'))
        try:
            await self.account.connect()
            me = await self.account.get_me()
            me.first_name  # noqa

            if not self.parameters.check_spamblock.value:
                self._log(_('MODULE-account_checker-account_is_alive'), color='green')
                await self.account.disconnect()
                await self.account.move_to_folder(files.alive_accounts_folder)
                return AccountCheckingResult.ALIVE

            # We need to check for spamblock
            spamblock_checker = SpamblockChecker(self.account)
            spamblock_checking_result = await spamblock_checker.check_for_spamlbock()
            if spamblock_checking_result == SpamblockCheckingResult.NO_SPAMBLOCK:
                self._log(_('MODULE-account_checker-account_is_alive'), color='green')
                await self.account.disconnect()
                await self.account.move_to_folder(files.alive_accounts_folder)
                return AccountCheckingResult.ALIVE
            elif spamblock_checking_result == SpamblockCheckingResult.TEMPORARY_SPAMBLOCK:
                self._log(_('MODULE-account_checker-temporary_spamblock'), color='yellow')
                await self.account.disconnect()
                await self.account.move_to_folder(files.temp_sb_accounts_folder)
                return AccountCheckingResult.TEMPORARY_SPAMBLOCK
            elif spamblock_checking_result == SpamblockCheckingResult.ETERNAL_SPAMLBOCK:
                self._log(_('MODULE-account_checker-eternal_spamblock'), color='yellow')
                await self.account.disconnect()
                await self.account.move_to_folder(files.et_sb_accounts_folder)
                return AccountCheckingResult.ETERNAL_SPAMBLOCK
            else:
                await self.account.disconnect()
                return print('amogus')

        except ConnectionError:
            self._log(_('MODULE-account_checker-connection_error'), color='red')
            await self.account.disconnect()
            return AccountCheckingResult.CONNECTION_ERROR
        except AttributeError:
            self._log(_('MODULE-account_checker-dead_after_connecting'), color='red')
            await self.account.disconnect()
            await self.account.move_to_folder(files.dead_accounts_folder)
            return AccountCheckingResult.DEAD_AFTER_CONNECTING
        except errors.PhoneNumberBannedError:
            self._log(_('MODULE-account_checker-phone_number_banned'), color='red')
            await self.account.disconnect()
            await self.account.move_to_folder(files.dead_accounts_folder)
            return AccountCheckingResult.PHONE_NUMBER_BANNED
        except errors.SessionRevokedError:
            self._log(_('MODULE-account_checker-reset_all_sessions'), color='red')
            await self.account.disconnect()
            await self.account.move_to_folder(files.dead_accounts_folder)
            return AccountCheckingResult.RESET_ALL_SESSIONS
        except errors.AuthKeyDuplicatedError:
            self._log(_('MODULE-account_checker-auth_key_duplicated'), color='red')
            await self.account.disconnect()
            await self.account.move_to_folder(files.dead_accounts_folder)
            return AccountCheckingResult.AUTH_KEY_DUPLICATED
        except errors.AuthKeyUnregisteredError:
            self._log(_('MODULE-account_checker-auth_key_unregistered'), color='red')
            await self.account.disconnect()
            await self.account.move_to_folder(files.dead_accounts_folder)
            return AccountCheckingResult.AUTH_KEY_UNREGISTERED
        except (errors.UserDeactivatedError, errors.UserDeactivatedBanError):
            self._log(_('MODULE-account_checker-deactivated'), color='red')
            await self.account.disconnect()
            await self.account.move_to_folder(files.dead_accounts_folder)
            return AccountCheckingResult.DEACTIVATED
        except sqlite3.OperationalError:
            self._log(_("ACCOUNT-database_locked").format(self.account.account_info.session_name), color='yellow')
            return AccountCheckingResult.OTHER_ERROR
        except BaseException as e:
            logger.exception(f'Error while checking account {self.account.account_info.session_name}')
            self._log(
                _('MODULE-account_checker-other_error').format(f'{type(e).__name__}: {str(e)}'),
                color='red'
            )
            await self.account.disconnect()
            return AccountCheckingResult.OTHER_ERROR
