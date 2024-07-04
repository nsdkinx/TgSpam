# -*- coding: utf-8 -*-

import asyncio
import itertools
import logging
import string
import traceback
from typing import Optional

from telethon import functions, types, errors

from account.telegram_account import TelegramAccount
from core.localization.interface import _
from core.taskpool import TaskPoolExecutor
from core.ui.ui_manager import UIManager as ui
from .audience_saver import AudienceSaver
from .parameters import AudienceParserParameters
from .errors import *

logger = logging.getLogger(__name__)


class DeepParser:

    def __init__(
            self,
            accounts: list[TelegramAccount],
            groups: list[str],
            parameters: AudienceParserParameters,
            audience_saver: AudienceSaver
    ):
        self.accounts = accounts
        self.groups = groups
        self.parameters = parameters
        self.audience_saver = audience_saver
        self._account_iterator = itertools.cycle(accounts)
        self._filter = parameters.filter.value()
        self._groups_to_stop_working = []

    @staticmethod
    def _log(text: str, account: TelegramAccount, group: str, color: Optional[str] = None):
        if color:
            return ui.log(
                f'[{color}]'
                f'[dim]({_("account")} {account.account_info.session_name}) '
                f'({_("group")} {group})[/dim] '
                f'{text}'
                f'[/{color}]'
            )
        return ui.log(
            f'[dim]({_("account")} {account.account_info.session_name}) '
            f'({_("group")} {group})[/dim] '
            f'{text}'
        )

    async def _parse_single_group(self, account: TelegramAccount, group: str, letter: str):
        if group in self._groups_to_stop_working:
            return
        if not account.is_connected():
            self._log(_("MODULE-base-connecting"), account, group)
            connecting_result = await account.connect_and_check()
            if not connecting_result:
                return None

        await account.acquire_lock()

        try:
            await account.get_entity(group)
        except (ValueError, errors.UsernameInvalidError):
            self._log(
                '[red]' + _("MODULE-audience_parser-parser_error").format(str(ChatNotFoundError())) + '[/red]',
                account, group
            )
            self._groups_to_stop_working.append(group)
            await account.release_lock()
            return
        except errors.ChatAdminRequiredError:
            self._log(
                '[red]' + _("MODULE-audience_parser-parser_error").format(str(NeedsAdminError())) + '[/red]',
                account, group
            )
            self._groups_to_stop_working.append(group)
            await account.release_lock()
            return
        except BaseException as e:
            logger.exception(f'Exception while getting entity in group {group}.')
            self._log(
                '[red]' + _("MODULE-audience_parser-error").format(str(e)) + '[/red]',
                account, group
            )
            self._groups_to_stop_working.append(group)
            await account.release_lock()
            return

        self._log(
            _("MODULE-audience_parser-deep_parsing_start_thread").format('[green]' + letter.upper() + '[/green]'),
            account, group
        )
        collected_users: list[types.User] = []
        offset = 0
        limit = 100
        while True:
            await asyncio.sleep(0)

            try:
                participants = await account(functions.channels.GetParticipantsRequest(
                    group, types.ChannelParticipantsSearch(letter), offset, limit, hash=0
                ))
            except errors.ChatAdminRequiredError:
                self._log(
                    '[red]' + _("MODULE-audience_parser-parser_error").format(str(NeedsAdminError())) + '[/red]',
                    account, group
                )
                self._groups_to_stop_working.append(group)
                return
            except BaseException as e:
                logger.exception(f'Exception while getting participants in group {group}.')
                self._log(
                    '[red]' + _("MODULE-audience_parser-error").format(str(e)) + '[/red]',
                    account, group
                )
                self._groups_to_stop_working.append(group)
                return

            if not participants.users:  # noqa
                break
            for user in participants.users:
                await asyncio.sleep(0)
                if user not in collected_users and self._filter.validate_user(user):
                    await self.audience_saver.write_user(user.username, group)
                    collected_users.append(user.username)
            offset += len(participants.users)
            # await _create_little_delay()

        self._log(
            _("MODULE-audience_parser-deep_thread_collected")
            .format(letter.upper(), len(collected_users)), account, group, color='green'
        )
        # await _create_little_delay()
        await account.release_lock()
        return

    async def start_working(self):
        for group in self.groups:
            try:
                task_pool = TaskPoolExecutor(max_size=10, collect_results=True)
                async with task_pool:
                    for letter in string.ascii_lowercase:
                        account = next(self._account_iterator)
                        await task_pool.submit(self._parse_single_group, account, group, letter)

                try:
                    parsed_count = await self.audience_saver.get_parsed_count_for_chat(group)
                    ui.log(
                        '[green]'
                        + _("MODULE-audience_parser-deep_chat_done").format(parsed_count, group)
                        + '[/green]'
                    )
                except KeyError:
                    pass
            except ParserError as e:
                ui.log('[red]' + _("MODULE-audience_parser-parser_error").format(str(e)) + '[/red]')
                continue
            except BaseException as e:
                logger.exception('DeepParser.start_working BaseException')
                ui.log('[red]' + _("MODULE-audience_parser-error").format(str(e)) + '[/red]')
                continue

        for account in self.accounts:
            await account.disconnect()
