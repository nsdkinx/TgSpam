# -*- coding: utf-8 -*-

import asyncio
from pathlib import Path
from datetime import datetime
from telethon.types import User

from core.filesystem.container import files
from core.localization.interface import _

from .inviting_result import InvitingResult


class TextReportManager:
    """Manages the report file"""

    def __init__(self, group: str):
        _date_str = datetime.now().strftime('%d.%m.%Y-%H-%M')
        self._group = group
        self._reports_folder = files.reports_folder
        self._current_session_folder = self._reports_folder / f'{_("MODULE-inviter-short_name")}-{_date_str}-{group}'
        self._file_lock = asyncio.Lock()

        self._total_invites_file = self._current_session_folder / f'{_("MODULE-inviter-total_invites_file")}.txt'
        self._successful_invites_file = self._current_session_folder / f'{_("MODULE-inviter-successful_invites_file")}.txt'
        self._privacy_restricted_file = self._current_session_folder / f'{_("MODULE-inviter-privacy_restricted_file")}.txt'
        self._failed_file = self._current_session_folder / f'{_("MODULE-inviter-failed_file")}.txt'
        self._invite_log_file = self._current_session_folder / f'{_("MODULE-inviter-log_file")}.txt'

        self._current_session_folder.mkdir(parents=True, exist_ok=True)
        self._total_invites_file.touch(exist_ok=True)
        self._successful_invites_file.touch(exist_ok=True)
        self._privacy_restricted_file.touch(exist_ok=True)
        self._failed_file.touch(exist_ok=True)
        self._invite_log_file.touch(exist_ok=True)

    async def _write(self, string: str, file: Path):
        async with self._file_lock:
            with file.open('a+', encoding='utf-8') as f:
                f.write(string + '\n')
        return True

    async def did_invite_user(self, user: User, inviting_result: InvitingResult):
        username = '@' + user.username
        await self._write(username, self._total_invites_file)
        if inviting_result == InvitingResult.OK:
            await self._write(username, self._successful_invites_file)
            await self._write(f'{username} => {self._group} => OK', self._invite_log_file)
        elif inviting_result == InvitingResult.PRIVACY_RESTRICTED:
            await self._write(username, self._privacy_restricted_file)
            await self._write(f'{username} => {self._group} => {_("MODULE-inviter-log_file-privacy_restricted")}', self._invite_log_file)
        else:
            await self._write(username, self._failed_file)
            await self._write(f'{username} => {self._group} => {_("MODULE-inviter-log_file-other")}', self._invite_log_file)

    async def write_final_stats_into_log(self):
        text = ""
        from .inviter_statistics import InviterStatistics
        text += '\n' + _("MODULE-inviter-results") + '\n'
        text += f'{_("MODULE-inviter-results-total_inviting_attempts")}: {InviterStatistics.get_total_inviting_attempts()}\n'
        text += f'{_("MODULE-inviter-results-successful_invites")}: {InviterStatistics.get_successful_invites()}\n'
        text += f'{_("MODULE-inviter-results-privacy_restricted")}: {InviterStatistics.privacy_restricted}\n'
        text += f'{_("MODULE-inviter-results-too_many_channels")}: {InviterStatistics.too_many_channels}\n'
        text += f'{_("MODULE-inviter-results-not_found")}: {InviterStatistics.not_found}\n'
        async with self._file_lock:
            with self._invite_log_file.open('a+', encoding='utf-8') as f:
                f.write(text)
        return
