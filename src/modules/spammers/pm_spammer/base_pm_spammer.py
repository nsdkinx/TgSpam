# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from pathlib import Path

from account.telegram_account import TelegramAccount
from typing import Optional
from telethon import types


class BasePMSpammer(ABC):
    """Provides a base class for all PM spammers"""

    @abstractmethod
    async def send_message(self, send_from: TelegramAccount, to: types.User, text: str, media: Optional[list[Path]]):
        raise NotImplementedError
