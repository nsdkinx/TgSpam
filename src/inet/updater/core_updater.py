# -*- coding: utf-8 -*-

import wget
import os
import logging

from inet.config import public_server_address
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _

logger = logging.getLogger(__name__)


class CoreUpdater:
    """Manages the updating of the .exe core"""

    @classmethod
    async def _delete_old_main_file_if_neccessary(cls):
        """Deletes the data/main_.exe leftover file if it exists"""
        try:
            if os.path.exists('data/main_.exe'):
                os.remove('data/main_.exe')
                logger.info(f'data/main_.exe did exist, so we removed it')
            return
        except BaseException:
            logger.exception(f'Exception at CoreUpdater._delete_old_main_file_if_neccessary')
            ui.log('[yellow]' + _("INET-updater-delete_old_main_file_error") + '[/yellow]')
            return

    @classmethod
    async def _download_main_updated_exe(cls):
        ui.log(_("INET-updater-downloading_exe_file"))
        try:
            wget.download(f'{public_server_address}/public/update/download', out='data/main_updated.exe')
            print()
            logger.info(f'{public_server_address}/public/update/download => OK: data/main_updated.exe')
            return
        except BaseException as e:
            logger.exception('Exception at CoreUpdater._download_main_updated_exe')
            raise  # this one is critical

    @classmethod
    async def _rename_main_exe(cls):
        try:
            os.rename('data/main.exe', 'data/main_.exe')
            logger.info(f'data/main.exe => data/main_.exe OK')
        except BaseException:
            logger.exception('Exception at CoreUpdater._rename_main_exe')
            raise  # this one is critical too

    @classmethod
    async def _rename_main_updated_exe(cls):
        try:
            os.rename('data/main_updated.exe', 'data/main.exe')
            logger.info('data/main_updated.exe => data/main.exe OK')
        except BaseException:
            logger.exception('Exception at CoreUpdater._rename_main_updated_exe')
            raise  # this one is critical as well

    @classmethod
    async def update_core(cls):
        await cls._delete_old_main_file_if_neccessary()
        await cls._download_main_updated_exe()
        await cls._rename_main_exe()
        await cls._rename_main_updated_exe()
        return
