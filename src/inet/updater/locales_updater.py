# -*- coding: utf-8 -*-

import os

import wget
import zipfile
import logging

from inet.config import public_server_address
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _

logger = logging.getLogger(__name__)


class LocalesUpdater:

    @classmethod
    async def _download_new_locales(cls):
        ui.log(_("INET-updater-downloading_locales"))
        try:
            wget.download(f'{public_server_address}/public/update/download_locales', out='data/locales.zip')
            print()
            logger.info(f'{public_server_address}/public/update/download_locales => OK: data/locales.zip')
        except BaseException:
            logger.exception('Exception in LocalesUpdater._download_new_locales')
            raise

    @classmethod
    async def _unpack_new_locales(cls):
        if not os.path.exists('data/locales.zip'):
            logger.error('tried to unpack locales, but data/locales.zip does not exist')
            raise RuntimeError('tried to unpack locales, but data/locales.zip does not exist')
        try:
            zip_file = zipfile.ZipFile('data/locales.zip')
            zip_file.extractall('data/locales/')
        except BaseException:
            logger.exception(f'Exception at LocalesUpdater._unpack_new_locales')
            raise

    @classmethod
    async def _delete_archive(cls):
        try:
            return os.remove('data/locales.zip')
        except BaseException:
            logger.exception('Exception at LocalesUpdater._delete_archive')
            return  # can be ignored

    @classmethod
    async def update_locales(cls):
        await cls._download_new_locales()
        await cls._unpack_new_locales()
        await cls._delete_archive()
        return
