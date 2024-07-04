# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from modules._base.parameters.module_parameter import ModuleParameter
from core.localization.interface import _
from core.filesystem.container import files
from core.ui.input_manager import InputManager as im
from ..core.content_selector import content_selector
from extras.audience_manager import AudienceManager
from extras.audience_selector import AudienceSelector

audience_manager = AudienceManager(files.audience_bases_folder)
audience_selector = AudienceSelector(audience_manager)


@dataclass
class PMSpammerParameters:
    content: ModuleParameter
    audience: ModuleParameter
    all_messages_limit: ModuleParameter
    messages_from_account_limit: ModuleParameter
    delay_between_messages: ModuleParameter

    @classmethod
    def ask_user(cls) -> PMSpammerParameters:
        content = content_selector.get_content_via_selector()
        audience = audience_selector.get_audience_base_via_selector()
        all_messages_limit = im.get_int_input(_("MODULE-pm_spammer-enter_limit"))
        messages_from_account_limit = im.get_int_input(_("MODULE-pm_spammer-enter_acct_limit"))
        delay_between_messages = im.get_range_input(_("MODULE-pm_spammer-enter_delay"))

        return cls(
            content=ModuleParameter(
                name=_("MODULE-pm_spammer-parameter-content"),
                value=content
            ),
            audience=ModuleParameter(
                name=_("MODULE-inviter-parameter-audience"),
                value=audience
            ),
            all_messages_limit=ModuleParameter(
                name=_("MODULE-inviter-parameter-all_invitings_limit"),
                value=all_messages_limit
            ),
            messages_from_account_limit=ModuleParameter(
                name=_("MODULE-inviter-parameter-invitings_from_account_limit"),
                value=messages_from_account_limit
            ),
            delay_between_messages=ModuleParameter(
                name=_("MODULE-inviter-parameter-delay_between_invitations"),
                value=delay_between_messages
            )
        )
