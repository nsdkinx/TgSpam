# -*- coding: utf-8 -*-

from .account_checker_parameters import AccountCheckerParameters
from .account_checker_worker import AccountCheckerWorker
from .results_presenter import ResultsPresenter
from core.settings.container import settings
from core.taskpool import TaskPoolExecutor
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _


class AccountCheckingController:
    """Controls the accounts."""

    def __init__(
            self,
            workers: list[AccountCheckerWorker],
            parameters: AccountCheckerParameters
    ):
        self.workers = workers
        self.parameters = parameters

    async def start_working(self):
        """Main function of account checker"""
        task_pool = TaskPoolExecutor(
            max_size=settings.concurrency_limit, collect_results=True
        )
        async with task_pool:
            for worker in self.workers:
                await task_pool.submit(worker.start_working)
        ui.log(_("MODULE-base-task_done"))
        ResultsPresenter.print_results(task_pool.results)
