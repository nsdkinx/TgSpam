# -*- coding: utf-8 -*-

from .account_checking_controller import AccountCheckingController
from .account_checker_parameters import AccountCheckerParameters
from modules._base.parameters.parameters_verifier import ParametersVerifier
from modules._base.parameters.parameters_verifying_result import (
    ParametersVerifyingResult,
    NeedToEditParameters,
    NeedToExitModule
)
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _
from .account_checker_worker import AccountCheckerWorker


async def module_main():
    while True:
        ui.paginate(_('MODULE-account_checker'))
        parameters = AccountCheckerParameters.ask_user()
        verifying_result = await ParametersVerifier.ask_to_verify_parameters(parameters)
        if verifying_result == NeedToExitModule:  # noqa
            return
        elif verifying_result == NeedToEditParameters:
            continue
        else:
            break

    workers: list[AccountCheckerWorker] = []

    for account in verifying_result.accounts:
        worker = AccountCheckerWorker(
            account, parameters
        )
        workers.append(worker)

    controller = AccountCheckingController(workers, parameters)
    await controller.start_working()

    ui.console.input('\n' + _('MODULE-base-press_enter_to_exit'))
