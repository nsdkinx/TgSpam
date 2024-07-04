# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from modules._base.parameters.module_parameter import ModuleParameter
from core.localization.interface import _
from core.filesystem.container import files
from core.ui.input_manager import InputManager as im
from extras.audience_manager import AudienceManager
from extras.audience_selector import AudienceSelector

audience_manager = AudienceManager(files.audience_bases_folder)
audience_selector = AudienceSelector(audience_manager)


@dataclass
class InviterParameters:
    group: ModuleParameter
    audience: ModuleParameter
    all_invitings_limit: ModuleParameter
    invitings_from_account_limit: ModuleParameter
    delay_between_invitations: ModuleParameter

    @classmethod
    def ask_user(cls) -> InviterParameters:
        group = im.get_username_input(_("MODULE-inviter-enter_group"))
        audience = audience_selector.get_audience_base_via_selector()
        all_invitings_limit = im.get_int_input(_("MODULE-inviter-enter_limit"))
        invitings_from_account_limit = im.get_int_input(_("MODULE-inviter-enter_acct_limit"))
        delay_between_invitations = im.get_range_input(_("MODULE-inviter-enter_delay"))

        return cls(
            group=ModuleParameter(
                name=_("MODULE-inviter-parameter-group"),
                value=group
            ),
            audience=ModuleParameter(
                name=_("MODULE-inviter-parameter-audience"),
                value=audience
            ),
            all_invitings_limit=ModuleParameter(
                name=_("MODULE-inviter-parameter-all_invitings_limit"),
                value=all_invitings_limit
            ),
            invitings_from_account_limit=ModuleParameter(
                name=_("MODULE-inviter-parameter-invitings_from_account_limit"),
                value=invitings_from_account_limit
            ),
            delay_between_invitations=ModuleParameter(
                name=_("MODULE-inviter-parameter-delay_between_invitations"),
                value=delay_between_invitations
            )
        )
