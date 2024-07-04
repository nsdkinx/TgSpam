# -*- coding: utf-8 -*-
from .errors import InviterError
from .parameters import InviterParameters
from .users_container import UsersContainer
from .inviter_worker import InviterWorker
from .limits_controller import LimitsController
from .text_report_manager import TextReportManager

from modules._base.parameters.parameters_verifier import ParametersVerifier
from modules._base.parameters.parameters_verifier import (
    ParametersVerifyingResult,
    NeedToExitModule,
    NeedToEditParameters
)
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _
from core.taskpool import TaskPoolExecutor
from core.settings.container import settings


async def module_main():
    while True:
        ui.paginate(_('MODULE-inviter'))

        try:
            parameters = InviterParameters.ask_user()
            verifying_result = await ParametersVerifier.ask_to_verify_parameters(parameters)
        except InviterError as e:
            ui.log(f'[red]{str(e)}[/red]')
            ui.console.input(_("MODULE-base-press_enter_to_exit"))
            return
        if verifying_result == NeedToExitModule:  # noqa
            return
        elif verifying_result == NeedToEditParameters:
            continue
        else:
            break

    users_container = UsersContainer(parameters.audience.value)
    limits_controller = LimitsController(
        parameters.all_invitings_limit.value, parameters.invitings_from_account_limit.value
    )
    text_report_manager = TextReportManager(parameters.group.value)

    workers = [
        InviterWorker(
            parameters=parameters,
            account=account,
            group=parameters.group.value,
            users_container=users_container,
            limits_controller=limits_controller,
            text_report_manager=text_report_manager
        )
        for account in verifying_result.accounts
    ]

    task_pool = TaskPoolExecutor(
        max_size=settings.concurrency_limit
    )
    async with task_pool:
        for worker in workers:
            await task_pool.submit(worker.start_inviting)

    ui.log(_("MODULE-base-task_done"))

    await text_report_manager.write_final_stats_into_log()

    from .results_presenter import ResultsPresenter
    results_presenter = ResultsPresenter(limits_controller)
    results_presenter.print_inviting_results()

    input()
