# -*- coding: utf-8 -*-

import logging
from typing import Optional

from account.telegram_account import TelegramAccount
from .filters import BaseFilter
from .parameters import AudienceParserParameters
from .audience_saver import AudienceSaver
from .errors import *

from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _

from telethon import errors

logger = logging.getLogger(__name__)


class SimpleParsingWorker:
    """Controls the parsing of a single chat
    only with account."""

    def __init__(
            self,
            group: str,
            account: TelegramAccount,
            parameters: AudienceParserParameters,
            audience_saver: AudienceSaver
    ):
        self.group = group  # will be replaced by an entity
        self._group_name = group
        self.account = account
        self.parameters = parameters
        self.audience_saver = audience_saver
        self._filter: BaseFilter = parameters.filter.value()
        logger.info(f'Initialized SimpleParsingWorker({account = }, {self.group = }, {self._filter = }')

    def _log(self, text: str, color: Optional[str] = None):
        if color:
            return ui.log(
                f'[{color}]'
                f'({_("account")} {self.account.account_info.session_name}) '
                f'({_("group")} {self._group_name}) '
                f'{text}'
                f'[/{color}]'
            )
        return ui.log(
            f'({_("account")} {self.account.account_info.session_name}) '
            f'({_("group")} {self._group_name}) '
            f'{text}'
        )

    async def _get_group_entity(self):
        try:
            return await self.account.get_entity(self.group)
        except (ValueError, errors.UsernameInvalidError) as e:
            raise ChatNotFoundError from e
        except errors.ChatAdminRequiredError as e:
            raise NeedsAdminError from e

    async def _start_parsing(self):
        try:
            async for participant in self.account.iter_participants(self.group):
                if self._filter.validate_user(participant):
                    await self.audience_saver.write_user(participant.username, self._group_name)
        except errors.ChatAdminRequiredError as e:
            raise NeedsAdminError from e
        return

    async def _start_working(self):
        self._log(_('MODULE-audience_parser-starting'))
        self.group = await self._get_group_entity()
        await self._start_parsing()
        try:
            parsed_count = await self.audience_saver.get_parsed_count_for_chat(self._group_name)
            self._log(
                _('MODULE-audience_parser-finished').format(parsed_count),
                color='green'
            )
        except KeyError:
            pass
        return

    async def start_working(self):
        """Error handling and connecting wrapper for starting the work"""
        await self.account.acquire_lock()
        self._log(_('MODULE-base-connecting'))
        connecting_result = await self.account.connect_and_check()
        if not connecting_result:
            await self.account.release_lock()
            return []

        try:
            await self._start_working()
        except ParserError as e:
            self._log(_("MODULE-audience_parser-parser_error").format(str(e)), color='red')
        except BaseException as e:
            self._log(_("MODULE-audience_parser-error").format(f'{type(e).__name__}: {str(e)}'), color='red')

        await self.account.disconnect()
        await self.account.release_lock()
        return
