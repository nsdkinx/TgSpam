# -*- coding: utf-8 -*-

import logging
from telethon import errors
from telethon.tl.functions.contacts import UnblockRequest

from account.telegram_account import TelegramAccount
from .spamblock_checking_result import SpamblockCheckingResult

logger = logging.getLogger(__name__)


class SpamblockChecker:
    """Checks the account on spamblock by talking to the Spam Info bot."""

    def __init__(self, account: TelegramAccount):
        self.account = account

    @staticmethod
    def _determine_spamblock_type_by_text(text: str):
        if len(text.splitlines()) == 1:
            return SpamblockCheckingResult.NO_SPAMBLOCK
        if 'UTC' in text and '202' in text:
            return SpamblockCheckingResult.TEMPORARY_SPAMBLOCK
        return SpamblockCheckingResult.ETERNAL_SPAMLBOCK

    async def check_for_spamlbock(self) -> SpamblockCheckingResult:
        if not self.account.is_connected():
            await self.account.connect()

        async with self.account.conversation('@SpamBot') as convo:
            try:
                await convo.send_message('/start')
            except errors.YouBlockedUserError:
                await self.account(UnblockRequest('@SpamBot'))
                await convo.send_message('/start')
            spambot_response = await convo.get_response()

        response_text = spambot_response.text
        logger.info(response_text)

        return self._determine_spamblock_type_by_text(response_text)
