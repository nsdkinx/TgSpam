# -*- coding: utf-8 -*-

import logging
import os.path
import sys

from .core_updater import CoreUpdater
from .locales_updater import LocalesUpdater
from .update_server_interactor import UpdateServerInteractor

from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _

logger = logging.getLogger(__name__)


class UpdateController:
    def __init__(
            self,
            core_updater: CoreUpdater,
            locales_updater: LocalesUpdater,
            update_server_interactor: UpdateServerInteractor
    ):
        self._core_updater = core_updater
        self._locales_updater = locales_updater
        self._update_server_interactor = update_server_interactor

    async def update(self):
        """Update main function."""
        if os.path.exists('smm_no_updates'):
            logger.info('Tried to update, but smm_no_updates exists. Returning')
            return
        if not await self._update_server_interactor.is_update_available():
            return

        try:
            await self._update_server_interactor.print_changelog()
            await self._core_updater.update_core()
            await self._locales_updater.update_locales()
        except BaseException:
            ui.log('[red]' + _("INET-updater-error") + '[/red]')
            ui.console.input(_("WARNING-using_conhost-input"))
            return

        ui.log(_("INET-updater-done"))
        ui.console.input()
        sys.exit(0)
