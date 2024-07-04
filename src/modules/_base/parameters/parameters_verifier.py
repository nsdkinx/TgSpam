# -*- coding: utf-8 -*-

import logging
from dataclasses import asdict
from typing import Union, Iterable
from rich.progress import Progress

from account.account_loader import AccountLoader
from account.telegram_account import TelegramAccount
from core.localization.interface import _
from core.range import AnyType
from core.settings.container import settings
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from proxy.model import Proxy
from proxy.proxy_checking_result import ProxyCheckingResult
from proxy.proxy_manager import ProxyManager
from extras.warnings_manager import WarningsManager
from .iparameters import IParameters
from .parameters_verifying_result import ParametersVerifyingResult, NeedToEditParameters, NeedToExitModule

logger = logging.getLogger(__name__)


class ParametersVerifier:
    """Runs before starting the module. It asks the user to verify module
    parameters and check the proxies."""

    @classmethod
    def _replace_proxies_on_all_linked_accs(cls, proxy: Proxy, accounts: list[TelegramAccount]):
        proxy_manager = ProxyManager.get_shared()
        new_software_proxy = proxy_manager.get_software_proxy()
        if not new_software_proxy:
            logger.error(f'Tried to change {proxy} on {len(accounts)} accounts, but there are no software proxies.')
            ui.print('[red]' + _("MODULE-base-no_proxies_to_change_to").format(len(accounts)) + '[/red]')
            new_software_proxy = None
        logger.info(f'Will change {proxy} to {new_software_proxy} on {len(accounts)} accounts')

        for account in accounts:
            if account.proxy == proxy:
                if not new_software_proxy:
                    account.change_proxy(new_software_proxy, write_to_json=False)
                else:
                    account.change_proxy(new_software_proxy)
                ui.log(
                    f'[yellow]' +
                    _("PROXY_MANAGER-replaced_proxy").format(account.account_info.session_file) +
                    '[/yellow]'
                )

        return True

    @classmethod
    async def check_proxies(cls, accounts: list[TelegramAccount]):
        """Checks the proxies with a cool progressbar.
        If a proxy is invalid, take a software proxy
        and write it into the JSON file"""
        proxy_manager = ProxyManager.get_shared()
        all_proxies = proxy_manager.get_all_proxies()

        if len(all_proxies) == 0:
            ui.print(f'[red]{_("MODULE-base-no_proxies_warning")}[/red]')
            return

        if not settings.check_proxy_before_work:
            return

        with Progress(console=ui.console) as progress:
            task = progress.add_task(_("MODULE-base-now_checking_proxy"), total=len(all_proxies))
            for proxy in all_proxies:
                checking_result = await proxy_manager.check_proxy(proxy)
                logger.info(f'Checking proxy {proxy} got result: {checking_result}')
                if checking_result != ProxyCheckingResult.ALIVE:
                    ui.print(
                        f'[red]- {_("MODULE-base-invalid_proxy").format(proxy.addr, proxy.port, proxy.username)} '
                        f'{checking_result.value}'
                    )
                    cls._replace_proxies_on_all_linked_accs(proxy, accounts)

                progress.advance(task)

        return

    @classmethod
    async def get_accounts(cls):
        WarningsManager.warn_if_accounts_in_alive_folder()
        account_loader = AccountLoader.get_shared()
        return account_loader.get_accounts()

    @classmethod
    async def ask_to_verify_parameters(cls, parameters: IParameters) -> Union[
            ParametersVerifyingResult, NeedToEditParameters, NeedToExitModule
    ]:
        """Main function. Renders the UI"""
        accounts = await cls.get_accounts()
        await cls.check_proxies(accounts)  # Check proxies before rendering banner
        accounts_count = len(accounts)
        proxies_count = ProxyManager.get_shared().total_count
        parameters_dict: dict[str, dict[str, AnyType]] = asdict(parameters)  # noqa
        # HACK
        # КОСТЫЛЬ ЕБАНЫЙ
        if hasattr(parameters, 'audience'):
            if parameters.audience.value:
                parameters_dict['audience']['value'] = parameters.audience.value

        if not accounts_count:
            ui.print(f'[red]{_("MODULE-base-no_accounts_error")}[/red]')
            ui.console.input(_("MODULE-base-press_enter_to_exit"))
            return NeedToExitModule

        print()
        ui.print_header(_('MODULE-base-everything_is_ready'))
        ui.print_key_and_value(
            _('MODULE-base-eir_banner-accounts'), accounts_count, inverse_colors=True, add_tabulation=True
        )
        ui.print_key_and_value(
            _('MODULE-base-eir_banner-proxies'), proxies_count, inverse_colors=True, add_tabulation=True
        )

        for parameter in parameters_dict.values():
            parameter, value = parameter.values()
            ui.print_key_and_value(parameter, value, inverse_colors=True, add_tabulation=True)

        # ui.console.input(ui.make_accented_text(_("MODULE-base-press_enter_to_start")))
        print()
        selection = im.select_from_list(
            _("MODULE-base-parameters-selection-prefix"),
            choices=[
                _("MODULE-base-parameters-selection-run_module"),
                _("MODULE-base-parameters-selection-need_to_edit_parameters"),
                _("MODULE-base-parameters-selection-need_to_exit_module")
            ],
            return_index=True
        )
        if selection == 1:
            return ParametersVerifyingResult(
                accounts=accounts
                # proxies=proxies
            )
        elif selection == 2:
            return NeedToEditParameters
        elif selection == 3:
            return NeedToExitModule
