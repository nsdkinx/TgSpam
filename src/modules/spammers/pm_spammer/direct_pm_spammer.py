# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional
from telethon import types
from account.telegram_account import TelegramAccount
from .base_pm_spammer import BasePMSpammer


class DirectPMSpammer(BasePMSpammer):
    """Sends the messages directly to user's PM"""

    def __init__(self) -> None:
        super().__init__()

    async def send_message(self, send_from: TelegramAccount, to: types.User, text: str, media: Optional[list[Path]]):
        client = send_from
        user = to
        if media:
            return await client.send_file(user, media, caption=text)
        else:
            return await client.send_message(user, text)
