# -*- coding: utf-8 -*-

from core.localization.interface import _
from core.ui.ui_manager import UIManager as ui
from ..limits_controller import LimitsController


# noinspection PyTypeChecker
class ResultsPresenter:
    """Pretty-prints pm spamming results via PMSpammerStatistics"""

    def __init__(
            self,
            limits_controller: LimitsController
    ):
        self._limits_controller = limits_controller

    def print_spamming_results(self):
        from .pm_spammer_statistics import PMSpammerStatistics
        ui.print_dashed_header(_("MODULE-pm_spammer-results"))
        ui.print_key_and_value(
            _("MODULE-pm_spammer-results-successful_sends"), PMSpammerStatistics.successful_sends
        )
        ui.print_key_and_value(
            _("MODULE-pm_spammer-results-not_found"), PMSpammerStatistics.not_found
        )
        print()
        ui.print_dashed_header(_("MODULE-pm_spammer-account_statistics"))
        for account_name, sends in self._limits_controller.get_account_sends_table().items():
            ui.print_key_and_value(account_name, sends)

        PMSpammerStatistics.clear()
