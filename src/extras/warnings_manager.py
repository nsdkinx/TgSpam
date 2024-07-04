# -*- coding: utf-8 -*-

import logging
from core.filesystem.container import files
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _

logger = logging.getLogger(__name__)


class WarningsManager:
    """Can warn a user if some condition
    is not right"""

    @classmethod
    def warn_if_accounts_in_alive_folder(cls):
        alive_accounts_count = len(list(files.alive_accounts_folder.glob('*.session')))
        accounts_count = len(list(files.accounts_folder.glob('*.session')))
        if alive_accounts_count > 0 and accounts_count == 0:
            logger.info(f'There are {alive_accounts_count} in alive accs folder and no loaded accounts. Warning user')
            ui.print(
                '[red]' + _("WARNING-accounts_in_alive_folder").format(alive_accounts_count) + '[/red]'
            )

    @classmethod
    def warn_if_using_conhost(cls):
        if ui.console.legacy_windows:
            logger.info('User is using conhost!')
            ui.print(
                '[yellow]' + _("WARNING-using_conhost") + '[/yellow]'
            )
            ui.console.input(_("WARNING-using_conhost-input"))

    @classmethod
    def display_deep_parser_banner(cls):
        logger.info('Displaying deep parser banner')
        ui.print('[yellow]' + _("WARNING-deep_parser") + '[/yellow]')
