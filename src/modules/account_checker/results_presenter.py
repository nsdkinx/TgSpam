# -*- coding: utf-8 -*-

from .account_checking_result import AccountCheckingResult
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _


class ResultsPresenter:
    """Processes the AccountCheckingResult values and prints a cool
    banner with checking results"""

    @classmethod
    def _get_amount_of_each_type_accs(
            cls,
            checking_results: list[AccountCheckingResult]
    ) -> dict[AccountCheckingResult, int]:
        return {
            checking_result: checking_results.count(checking_result)
            for checking_result in checking_results
        }

    @classmethod
    def print_results(cls, checking_results: list[AccountCheckingResult]):
        ui.print_dashed_header(_('MODULE-account_checker-results-header'))
        for checking_result, amount in cls._get_amount_of_each_type_accs(checking_results).items():
            ui.print_key_and_value(
                key=checking_result.value,
                value=amount,
                add_tabulation=True
            )
