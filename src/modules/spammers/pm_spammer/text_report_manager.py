# -*- coding: utf-8 -*-

import asyncio
from datetime import datetime
from pathlib import Path
from core.localization.interface import _
from core.filesystem.container import files
from telethon.types import User

from ..core.content import Content
from ..send_result import SendResult


class TextReportManager:
    """This class is responsible for writing text logs of the PM spammer"""

    def __init__(self):
        _date_str = datetime.now().strftime('%d.%m.%Y-%H-%M')
        self._file_lock = asyncio.Lock()
        self._current_session_folder = files.reports_folder / f'{_("MODULE-pm_spammer-short_name")}-{_date_str}'

        self._spammer_log_file = self._current_session_folder / f'{_("MODULE-pm_spammer-log_file")}.txt'
        self._total_sends_file = self._current_session_folder / f'{_("MODULE-pm_spammer-total_sends_file")}.txt'
        self._successful_sends_file = self._current_session_folder / f'{_("MODULE-pm_spammer-successful_sends_file")}.txt'
        self._not_found_file = self._current_session_folder / f'{_("MODULE-pm_spammer-not_found_file")}.txt'

        self._current_session_folder.mkdir(parents=True, exist_ok=True)
        self._total_sends_file.touch(exist_ok=True)
        self._successful_sends_file.touch(exist_ok=True)
        self._not_found_file.touch(exist_ok=True)

    async def _write(self, string: str, file: Path):
        async with self._file_lock:
            with file.open('a+', encoding='utf-8') as f:
                f.write(string + '\n')
        return True

    async def did_send_message(self, user: User, send_result: SendResult, content: Content):
        username = '@' + user.username
        await self._write(username, self._total_sends_file)
        if send_result == SendResult.OK:
            await self._write(username, self._successful_sends_file)
            await self._write(f'{username} => {content.name} => OK', self._spammer_log_file)
        elif send_result == SendResult.NOT_FOUND:
            await self._write(username, self._not_found_file)
            await self._write(f'{username} => {content.name} => {_("not_found")}', self._spammer_log_file)
        else:
            print(f'!!! at modules.spammers.pm_spammer.text_report_manager')
            print(f'!!! TextReportManager.did_send_message(user={user}, send_result={send_result}, content={content})')
            print(f'!!! did meet else statement')

    async def write_final_stats_into_log(self):
        text = ""
        from .pm_spammer_statistics import PMSpammerStatistics
        text += '\n--- ' + _("MODULE-pm_spammer-results") + ' ---\n'
        text += f'{_("MODULE-pm_spammer-results-total_sends")}: {PMSpammerStatistics.get_total_send_attempts()}\n'
        text += f'{_("MODULE-pm_spammer-results-successful_sends")}: {PMSpammerStatistics.successful_sends}\n'
        text += f'{_("MODULE-pm_spammer-results-not_found")}: {PMSpammerStatistics.not_found}\n'
        async with self._file_lock:
            with self._spammer_log_file.open('a+', encoding='utf-8') as f:
                f.write(text)
        return
