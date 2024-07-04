# -*- coding: utf-8 -*-

from core.settings.container import settings
from core.taskpool import TaskPoolExecutor
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _
from .direct_pm_spammer import DirectPMSpammer
from .parameters import PMSpammerParameters
from modules._base.parameters.parameters_verifier import ParametersVerifier
from modules._base.parameters.parameters_verifying_result import (
    ParametersVerifyingResult,
    NeedToEditParameters,
    NeedToExitModule
)
from .pm_spammer_worker import PMSpammerWorker
from .text_report_manager import TextReportManager
from ..errors import SpammerError
from ..users_container import UsersContainer
from ..limits_controller import LimitsController
from inet.telemetry_manager import TelemetryManager

telemetry_manager = TelemetryManager.get_shared()


async def module_main():
    while True:
        try:
            parameters = PMSpammerParameters.ask_user()
        except SpammerError as e:
            ui.log(f'[red]{e}[/red]')
            ui.console.input(_("MODULE-base-press_enter_to_exit"))
            return
        parameters_verifying_result = await ParametersVerifier.ask_to_verify_parameters(parameters)
        if parameters_verifying_result == NeedToEditParameters:
            continue
        elif parameters_verifying_result == NeedToExitModule:
            return
        else:
            break

    users_container = UsersContainer(parameters.audience.value)
    pm_spammer = DirectPMSpammer()
    limits_controller = LimitsController(
        parameters.all_messages_limit.value, parameters.messages_from_account_limit.value
    )
    text_report_manager = TextReportManager()
    workers = [
        PMSpammerWorker(
            pm_spammer=pm_spammer,
            parameters=parameters,
            account=account,
            users_container=users_container,
            limits_controller=limits_controller,
            text_report_manager=text_report_manager
        ) for account in parameters_verifying_result.accounts
    ]

    task_pool = TaskPoolExecutor(
        max_size=settings.concurrency_limit
    )
    async with task_pool:
        for worker in workers:
            await task_pool.submit(worker.start_spamming)

    ui.log(_("MODULE-base-task_done"))

    await text_report_manager.write_final_stats_into_log()

    from .results_presenter import ResultsPresenter
    results_presenter = ResultsPresenter(limits_controller)
    results_presenter.print_spamming_results()

    from .pm_spammer_statistics import PMSpammerStatistics
    await telemetry_manager.send_telemetry_message(
        __name__,
        f'Разослано {PMSpammerStatistics.get_total_send_attempts()} сообщений {len(workers)} воркерами'
    )

    input()

    return
