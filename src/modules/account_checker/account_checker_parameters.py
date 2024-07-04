# -*- coding: utf-8 -*-

from dataclasses import dataclass
from core.ui.input_manager import InputManager as im
from core.localization.interface import _
from modules._base.parameters.module_parameter import ModuleParameter


@dataclass
class AccountCheckerParameters:
    check_spamblock: ModuleParameter

    @classmethod
    def ask_user(cls):
        return cls(
            check_spamblock=ModuleParameter(
                name=_("MODULE-account_checker-check_for_spamblock"),
                value=im.get_bool_input(_("MODULE-account_checker-check_for_spamblock"))
            )
        )
