# -*- coding: utf-8 -*-

import asyncio
import itertools

from pathlib import Path
from telethon.types import User
from account.telegram_account import TelegramAccount


class AudienceSaver:
    """Controls the audience collected by all accounts and
    writes the audience to the file in real time"""

    def __init__(self, file: Path):
        self.file = file
        if not file.exists():
            file.touch()
        self._participants_by_chat: dict[str, set[str]] = {}

    @property
    def all_participants(self) -> list[str]:
        return list(itertools.chain(*self._participants_by_chat.values()))

    @staticmethod
    def _convert_user_to_string(user: str) -> str:
        return f'@{user}'

    def _add_user_for_chat(self, user: str, chat: str):
        if chat not in self._participants_by_chat:
            self._participants_by_chat[chat] = {user}
        else:
            self._participants_by_chat[chat].add(user)

    async def write_user(self, user: str, chat: str):
        if user in self.all_participants:
            return
        self._add_user_for_chat(user, chat)
        with self.file.open('a+', encoding='utf-8') as f:
            f.write(self._convert_user_to_string(user) + '\n')
        return

    async def get_parsed_count_for_chat(self, chat: str) -> int:
        return len(self._participants_by_chat[chat])
