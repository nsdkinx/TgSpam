# -*- coding: utf-8 -*-

from core.localization.interface import _
from core.ui.ui_manager import UIManager as ui
from modules.inviter.limits_controller import LimitsController


# noinspection PyTypeChecker
class ResultsPresenter:
    """Pretty-prints inviting results via InviterStatistics"""

    def __init__(
            self,
            limits_controller: LimitsController
    ):
        self.limits_controller = limits_controller

    def print_inviting_results(self):
        from .inviter_statistics import InviterStatistics
        ui.print_dashed_header(_("MODULE-inviter-results"))
        ui.print_key_and_value(
            _("MODULE-inviter-results-total_inviting_attempts"), InviterStatistics.get_total_inviting_attempts()
        )
        ui.print_key_and_value(
            _("MODULE-inviter-results-successful_invites"), InviterStatistics.get_successful_invites(),
        )
        # ui.print_key_and_value(
        #     _("MODULE-inviter-results-unable_to_invite"), InviterStatistics.get_unable_to_invite()
        # )
        ui.print_key_and_value(
            _("MODULE-inviter-results-privacy_restricted"), InviterStatistics.privacy_restricted
        )
        ui.print_key_and_value(
            _("MODULE-inviter-results-too_many_channels"), InviterStatistics.too_many_channels
        )
        ui.print_key_and_value(
            _("MODULE-inviter-results-not_found"), InviterStatistics.not_found
        )
        ui.print_key_and_value(
            _("MODULE-inviter-results-instantly_removed"), InviterStatistics.instantly_removed
        )
        print()
        ui.print_dashed_header(_("MODULE-inviter-account_statistics"))
        for account_name, invites in self.limits_controller.get_account_invites_table().items():
            ui.print_key_and_value(account_name, invites)

        InviterStatistics.clear()
