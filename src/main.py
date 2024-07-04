# -*- coding: utf-8 -*-
"""TgSpam client program main file."""

import sys
if len(sys.argv) == 2:
    # Argument parsing
    command = sys.argv[1]
    if command == '--version':
        try:
            from core.release_info import application_name, application_version
            print(f'{application_name} {application_version}')
            sys.exit(0)
        except (ModuleNotFoundError, ImportError):
            print('???')
            sys.exit(1)


import asyncio
import logging
import sys
from pathlib import Path


try:
    from core.ui.ui_manager import UIManager as ui
    from core.ui.input_manager import InputManager as im
    from core.release_info import application_name, application_version
    from extras.warnings_manager import WarningsManager
    from core.utils import DEBUG_MODE

    ui.set_window_title(f'{application_name} {application_version}')
except BaseException as e:
    print(f'--- !!! Pre-init app exception !!! ---')
    from core.utils.error_utils import format_exception

    format_exception(e)
    input()
    sys.exit(1)

# Setup logging

LOG_FILE_PATH = Path(f'data/tgspam.log')

logging.getLogger('telethon.network.mtprotosender').disabled = True
logging.getLogger('telethon.extensions.messagepacker').disabled = True
logging.getLogger('telethon.client.updates').disabled = True
logging.getLogger('telethon.network.connection.connection').disabled = True
logging.getLogger('telethon.crypto.libssl').disabled = True
logging.getLogger('telethon.crypto.aes').disabled = True

date_format = '%d.%m.%Y %H:%M:%S'
logging_format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'

if DEBUG_MODE:
    from rich.logging import RichHandler
    handlers = [
        RichHandler(show_time=False),
        logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
    ]
else:
    handlers = [
        logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
    ]

logging.basicConfig(
    format=logging_format,
    datefmt=date_format,
    handlers=handlers,
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
logger.info(f'-*-*-*- Starting application... -*-*-*-')

from core.exception_hook import global_exception_hook
sys.excepthook = global_exception_hook

# Setup localization

try:
    from core.localization.interface import _
    logger.info('Localization setup success')
except BaseException as e:
    logger.exception('Critical error while loading localization.')
    input(f'Critical error while loading localization.')
    sys.exit(1)


async def main():
    WarningsManager.warn_if_using_conhost()

    # Loading containers and consumables

    import modules
    from account.account_loader import AccountLoader
    from modules._base.modules_repository import ModulesRepository
    from modules._base.module_selector import ModuleSelector
    from proxy.software_proxy_container import SoftwareProxyContainer
    from proxy.proxy_manager import ProxyManager
    from core.filesystem.container import files

    software_proxy_container = SoftwareProxyContainer.make_from_file(files.proxy_file)
    proxy_manager = ProxyManager()

    account_loader = AccountLoader(files.accounts_folder)
    modules_repository = ModulesRepository(modules)
    module_selector = ModuleSelector(modules_repository)

    while True:
        # --- Main menu page ---
        ui.paginate(_("MENU-header"))
        ui.log(_("MENU-welcome").format(
            ui.make_accented_text(application_name),
            ui.make_accented_text(application_version)
        ))

        ui.log(_("MENU-consumables_stats").format(
            ui.make_accented_text(account_loader.total_accounts, highlight_zero=True),
            ui.make_accented_text(proxy_manager.total_count, highlight_zero=True)
        ))
        print()

        await module_selector.select_and_run_module()


if __name__ == '__main__':
    asyncio.run(main())
