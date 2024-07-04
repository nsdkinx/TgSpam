# -*- coding: utf-8 -*-

import asyncio
from core.settings.container import settings
from core.range import Range
from core.localization.interface import _
from core.ui.ui_manager import UIManager as ui


class DelaysManager:
    """Can wait several fixed delays like thread start delay
    DEPRECATED, DON'T USE!!!"""

    @classmethod
    async def wait_thread_start_delay(cls):
        thread_start_delay = Range.make_from_text_string(settings.thread_start_delay)
        random_number = thread_start_delay.make_random_number()
        ui.log(
            _('DELAYS_MANAGER-waiting_thread_start_delay').format(random_number)
        )
        return await asyncio.sleep(random_number)

    @classmethod
    async def wait_delay_from_str(cls, delay: str):
        """Helper method to wait a delay that is written
        in a string (like 3-5)"""
        random_number = Range.make_from_text_string(delay).make_random_number()
        ui.log(_('DELAYS_MANAGER-waiting').format(random_number))
        return await asyncio.sleep(random_number)

    @classmethod
    async def wait_peer_flood(cls):
        """Lets the account that got PeerFloodError rest a little bit.
        Logging is handled by the caller"""
        random_number = Range(10, 15).make_random_number()
        return await asyncio.sleep(random_number)

    @classmethod
    async def wait_flood_wait(cls, seconds: int):
        """Can wait a floodwait"""
        wait_time = seconds + 7.4
        ui.log(_("DELAYS_MANAGER-wait_flood_wait").format(seconds))
        return await asyncio.sleep(wait_time)
