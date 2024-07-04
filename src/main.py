# -*- coding: utf-8 -*-
"""SMM-SOFT client program main file."""

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

# --- Initialize Sentry ---
try:
    import sentry_sdk
    sentry_sdk.init(
        dsn="https://95252cd5a7ea4a6ca0f65362460f7c54@o4505503923109888.ingest.sentry.io/4505581738131456",
        traces_sample_rate=1.0
    )
except BaseException as e:
    print('Uh oh! Looks like you got a corrupted SMM-SOFT build.')
    print('The program failed to start with an error.')
    print('Please report this to the support team.')
    print('--------------------------------------')
    print('Ой! Кажется вам попался сломанный билд SMM-SOFT.')
    print('Программе не удалось запуститься из-за критической ошибки.')
    print('Пожалуйста, обратитесь в техническую поддержку.')
    print('--------------------------------------')
    print(f'{type(e).__name__}: {str(e)} || at sentry init')
    input()
    import sys
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
except FileNotFoundError:
    print('Не запускайте SMM-SOFT напрямую из .exe-файла.')
    print('Используйте файл Запуск.bat в папке выше.')
    print('---')
    print('Do not launch SMM-SOFT directly from the .exe file.')
    print('Use the .bat file in an upper folder.')
    input()
    sys.exit(1)
except BaseException as e:
    print(f'--- !!! Pre-init app exception !!! ---')
    from core.utils.error_utils import format_exception

    format_exception(e)
    input()
    sys.exit(1)

# Setup logging

LOG_FILE_PATH = Path(f'data/smmsoft.log')

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

from core.computer_info_logging import log_computer_info
log_computer_info()

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
    from inet.updater.update_controller import UpdateController
    from inet.updater.core_updater import CoreUpdater
    from inet.updater.locales_updater import LocalesUpdater
    from inet.updater.update_server_interactor import UpdateServerInteractor
    core_updater = CoreUpdater()
    locales_updater = LocalesUpdater()
    update_server_interactor = UpdateServerInteractor()
    update_controller = UpdateController(core_updater, locales_updater, update_server_interactor)
    await update_controller.update()

    with ui.wrap_with_header(_("ONBOARDING-program_activation_header")):
        import inet.config
        from inet.authorizer import Authorizer
        from inet.errors import InetError
        from inet.hardware_config import HardwareConfig
        from inet.encrypted_client import EncryptedClient
        from inet.license_key_storage import LicenseKeyStorage
        from inet.telemetry_manager import TelemetryManager
        from core.filesystem.container import files

        license_key_storage = LicenseKeyStorage(files.license_key_file)
        encrypted_client = EncryptedClient(inet.config.encrypted_server_address)
        license_key = license_key_storage.read_key()
        authorizer = Authorizer(encrypted_client)
        try:
            await authorizer.authorize(license_key, HardwareConfig.bios_serial)
            license_key_storage.write_key(license_key)
        except InetError as e:
            logger.exception('InetError.')
            ui.print(_("INET-inet_error").format(str(e)))
            ui.console.input(_("MODULE-base-press_enter_to_exit"))
            sys.exit(1)
        except BaseException as e:
            logger.exception('Error while authorizing.')
            ui.print(_("INET-error").format(str(e)))
            ui.console.input(_("MODULE-base-press_enter_to_exit"))
            sys.exit(1)

        telemetry_manager = TelemetryManager(encrypted_client)
        await telemetry_manager.send_telemetry_message('main', 'Софт запущен!')

    # Loading containers and consumables

    import modules
    from account.account_loader import AccountLoader
    from modules._base.modules_repository import ModulesRepository
    from modules._base.module_selector import ModuleSelector
    from proxy.software_proxy_container import SoftwareProxyContainer
    from proxy.proxy_manager import ProxyManager

    software_proxy_container = SoftwareProxyContainer.make_from_file(files.proxy_file)
    proxy_manager = ProxyManager()

    # for proxy in proxy_file.iter_proxies():
    #     checking_result = await ProxyChecker.check_single_proxy(proxy)
    #     print(proxy)
    #     print(checking_result)
    #
    # input()

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
        if authorizer.license.expiry_days >= 900:
            ui.log(_("MENU-license_expiry-eternal_license"))
        else:
            ui.log(_("MENU-license_expiry").format(
                ui.make_accented_text(authorizer.license.expiry_days)
            ))
        ui.log(_("MENU-consumables_stats").format(
            ui.make_accented_text(account_loader.total_accounts, highlight_zero=True),
            ui.make_accented_text(proxy_manager.total_count, highlight_zero=True)
        ))
        print()

        await module_selector.select_and_run_module()


if __name__ == '__main__':
    asyncio.run(main())
