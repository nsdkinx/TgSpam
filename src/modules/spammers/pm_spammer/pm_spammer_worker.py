# -*- coding: utf-8 -*-

import asyncio
import random
import logging

from telethon import types, errors

from account.telegram_account import TelegramAccount
from modules.spammers.pm_spammer.parameters import PMSpammerParameters
from .base_pm_spammer import BasePMSpammer
from .pm_spammer_statistics import PMSpammerStatistics
from .text_report_manager import TextReportManager
from ..core.content import Content
from ..send_result import SendResult
from ..users_container import UsersContainer
from ..limits_controller import LimitsController
from ..errors import SpammerError, OutOfUsersError, TooLongFloodWaitError, AccountSpamblockedError
from core.settings.container import settings
from core.range import Range
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _

logger = logging.getLogger(__name__)


class PMSpammerWorker:

    def __init__(
            self,
            pm_spammer: BasePMSpammer,
            parameters: PMSpammerParameters,
            account: TelegramAccount,
            users_container: UsersContainer,
            limits_controller: LimitsController,
            text_report_manager: TextReportManager
    ):
        self.working = asyncio.Event()
        self._pm_spammer = pm_spammer
        self._parameters = parameters
        self._account = account
        self._users_container = users_container
        self._limits_controller = limits_controller
        self._text_report_manager = text_report_manager
        self._peer_flood_count = 0
        self._peer_flood_limit = settings.peer_flood_limit
        self._sleep_range = Range.make_from_text_string(parameters.delay_between_messages.value)
        self._content: Content = parameters.content.value

    def _log(self, text: str, color: str = None):
        if color:
            return ui.log(
                f'[{color}]'
                f'({_("account")} {self._account.account_info.session_name}) '
                f'{text}'
                f'[/{color}]'
            )
        return ui.log(
            f'({_("account")} {self._account.account_info.session_name}) '
            f'{text}'
        )

    async def _prepare_for_work(self):
        return

    async def _send_one_user(self):
        try:
            user: str = self._users_container.take_user()
        except StopIteration:
            raise OutOfUsersError

        try:
            self._limits_controller.record_send(self._account)
        except SpammerError:
            raise  # so we don't get incremented

        try:
            user: types.User = await self._account.get_entity(user)
        except (ValueError, errors.UsernameInvalidError):
            self._log(_("MODULE-spammer-user_not_found").format(user), color='red')
            PMSpammerStatistics.not_found += 1
            await self._text_report_manager.did_send_message(user, SendResult.NOT_FOUND, self._content)
            return

        try:
            _text = random.choice(self._content.texts)
            text_name = _text.name
            text = _text.get_text()
            await self._pm_spammer.send_message(
                send_from=self._account,
                to=user,
                text=text,
                media=self._content.media
            )
            self._log(_("MODULE-pm_spammer-success_send").format(f'@{user.username}', text_name), color='green')
            PMSpammerStatistics.successful_sends += 1
            await self._text_report_manager.did_send_message(user, SendResult.OK, self._content)
        except errors.FloodWaitError as e:
            if e.seconds >= 800:
                raise TooLongFloodWaitError(e.seconds)
            self._log(
                _("MODULE-inviter-flood_wait").format(e.seconds),
                color='yellow'
            )  # TODO: adapt to spammer
            for _i in range(e.seconds + 7):
                await asyncio.sleep(0)
                await asyncio.sleep(1)
            return
        except errors.PeerFloodError:
            self._peer_flood_count += 1
            if self._peer_flood_count >= self._peer_flood_limit:
                raise AccountSpamblockedError
            else:
                self._log(_("MODULE-inviter-spamblock_error").format(self._peer_flood_count), color='yellow')  # TODO: adapt to spammer
                await asyncio.sleep(8.43)

        return

    async def _sleep(self):
        wait_time = self._sleep_range.make_random_number()
        self._log(_("MODULE-inviter-sleep").format(wait_time))
        await asyncio.sleep(wait_time)

    async def start_spamming(self):
        if self._limits_controller.is_overall_limit_hit():
            return

        self._log(_("MODULE-base-connecting"))
        connection_result = await self._account.connect_and_check()
        if not connection_result:
            return

        await self._account.acquire_lock()
        self.working.set()

        try:
            await self._prepare_for_work()
            while self.working.is_set():
                await asyncio.sleep(0)
                await self._send_one_user()
                await self._sleep()
        except SpammerError as e:
            self._log(_("MODULE-spammers-spammer_error").format(str(e)), color='red')
        except BaseException as e:
            logger.exception('Error in PMSpammerWorker.start_spamming')
            self._log(_("MODULE-spammers-error").format(f'{type(e).__name__}: {str(e)}'), color='red')

        await self._account.disconnect()
        await self._account.release_lock()
        self._log(_("MODULE-base-thread_stopped"))
        return
