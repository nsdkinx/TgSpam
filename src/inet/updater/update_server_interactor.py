# -*- coding: utf-8 -*-

from typing import Union
import aiohttp
import logging

from core.release_info import application_version
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _
from inet.config import public_server_address

logger = logging.getLogger(__name__)
headers = {'User-Agent': f'SMM-SOFT/{application_version}'}


class UpdateServerInteractor:

    @classmethod
    async def _make_server_request(cls, request: str, return_text: bool = False) -> Union[str, dict]:
        async with aiohttp.ClientSession(public_server_address, headers=headers) as session:
            response = await session.get(request)
            logger.info(f'GET {public_server_address}{request} => {response}')
            if return_text:
                return await response.text(encoding='utf-8')
            else:
                return await response.json(encoding='utf-8')

    @classmethod
    async def is_update_available(cls) -> bool:
        try:
            json_data = await cls._make_server_request(f'/public/update/check?app_version={application_version}')
            if json_data['need_to_update']:
                ui.log(_("INET-updater-update_available").format(application_version, json_data['latest_version']))
                return True
            return False
        except BaseException:
            logger.exception('Exception in UpdateChecker.is_update_available')
            raise

    @classmethod
    async def print_changelog(cls) -> None:
        try:
            changelog = await cls._make_server_request('/public/update/changelog', return_text=True)
            changelog = changelog.removeprefix('"').removesuffix('"').replace('-sep-', '\n')
            print()
            ui.print_dashed_header(_('INET-updater-changelog'))
            ui.print(changelog)
            print()
            return
        except BaseException:
            logger.exception('Error in UpdateServerInteractor.print_changelog')
            return
