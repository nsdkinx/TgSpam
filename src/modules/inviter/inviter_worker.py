# -*- coding: utf-8 -*-

import asyncio
import logging
from typing import Union

from telethon import functions, types, errors

from account.telegram_account import TelegramAccount
from core.localization.interface import _
from core.ui.ui_manager import UIManager as ui
from core.range import Range
from core.settings.container import settings
from .errors import *

from .inviter_statistics import InviterStatistics
from .limits_controller import LimitsController
from .parameters import InviterParameters
from .text_report_manager import TextReportManager
from .users_container import UsersContainer
from .inviting_result import InvitingResult

_logger = logging.getLogger(__name__)


class InviterWorker:
    """Controls the actions of a single account while inviting"""

    def __init__(
            self,
            parameters: InviterParameters,
            account: TelegramAccount,
            group: Union[str, types.Channel],
            users_container: UsersContainer,
            limits_controller: LimitsController,
            text_report_manager: TextReportManager
    ):
        self.working = asyncio.Event()
        self._parameters = parameters
        self._account = account
        self._group = group  # will be changed to an entity later
        self._group_name = group
        self._users_container = users_container
        self._limits_controller = limits_controller
        self._text_report_manager = text_report_manager
        self._peer_flood_count = 0
        self._peer_flood_limit = settings.peer_flood_limit
        self._sleep_range = Range.make_from_text_string(parameters.delay_between_invitations.value)

    def _log(self, text: str, color: str = None):
        if color:
            return ui.log(
                f'[{color}]'
                f'({_("account")} {self._account.account_info.session_name}) '
                f'({_("group")} {self._group_name}) '
                f'{text}'
                f'[/{color}]'
            )
        return ui.log(
            f'({_("account")} {self._account.account_info.session_name}) '
            f'({_("group")} {self._group_name}) '
            f'{text}'
        )

    async def _prepare_for_work(self):
        try:
            self._group = await self._account.get_entity(self._group)
        except ValueError:
            raise ChatNotFoundError(self._group)

        try:
            await self._account(functions.channels.JoinChannelRequest(self._group))
            self._log(_('MODULE-inviter-joined'))
        except errors.UserAlreadyParticipantError:
            pass

        return

    async def _invite_one_user(self):
        try:
            user: str = self._users_container.take_user()
        except StopIteration:
            raise OutOfUsersError

        try:
            self._limits_controller.record_invite(self._account)
        except InviterError:
            raise  # so we don't get incremented

        try:
            user: types.User = await self._account.get_entity(user)
        except (ValueError, errors.UsernameInvalidError):
            self._log(_("MODULE-inviter-user_not_found").format(user), color='red')
            InviterStatistics.not_found += 1
            return

        try:
            await self._account(functions.channels.InviteToChannelRequest(self._group, [user]))
            participants = await self._account(functions.channels.GetParticipantsRequest(
                self._group, types.ChannelParticipantsSearch(user.username), offset=0, limit=1, hash=0
            ))
            if not participants.participants:
                self._log(_('MODULE-inviter-instantly_removed').format(f'@{user.username}'), color='red')
                InviterStatistics.instantly_removed += 1
                await self._text_report_manager.did_invite_user(user, InvitingResult.OTHER)
            else:
                self._log(_('MODULE-inviter-success_invite').format(f'@{user.username}'), color='green')
                InviterStatistics.successful_invites += 1
                await self._text_report_manager.did_invite_user(user, InvitingResult.OK)
        except errors.FloodWaitError as e:
            if e.seconds >= 800:
                raise TooLongFloodWaitError(e.seconds)
            self._log(
                _("MODULE-inviter-flood_wait").format(e.seconds),
                color='yellow'
            )
            for _i in range(e.seconds + 7):
                await asyncio.sleep(0)
                await asyncio.sleep(1)
            return
        except errors.UserPrivacyRestrictedError:
            self._log(_("MODULE-inviter-privacy_restricted").format(f'@{user.username}'), color='yellow')
            InviterStatistics.privacy_restricted += 1
            await self._text_report_manager.did_invite_user(user, InvitingResult.PRIVACY_RESTRICTED)
        except errors.UserChannelsTooMuchError:
            self._log(_("MODULE-inviter-channels_too_much").format(f'@{user.username}'), color='yellow')
            InviterStatistics.too_many_channels += 1
            await self._text_report_manager.did_invite_user(user, InvitingResult.OTHER)
        except errors.PeerFloodError:
            self._peer_flood_count += 1
            if self._peer_flood_count >= self._peer_flood_limit:
                raise AccountSpamblockedError
            else:
                self._log(_("MODULE-inviter-spamblock_error").format(self._peer_flood_count), color='yellow')
                await asyncio.sleep(8.43)

    async def _sleep(self):
        wait_time = self._sleep_range.make_random_number()
        self._log(_("MODULE-inviter-sleep").format(wait_time))
        await asyncio.sleep(wait_time)

    async def start_inviting(self):
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
                await self._invite_one_user()
                await self._sleep()
        except InviterError as e:
            self._log(_("MODULE-inviter-inviter_error").format(str(e)), color='red')
        except BaseException as e:
            self._log(_("MODULE-inviter-error").format(f'{type(e).__name__}: {str(e)}'), color='red')

        await self._account.disconnect()
        await self._account.release_lock()
        self._log(_("MODULE-base-thread_stopped"))
        return
