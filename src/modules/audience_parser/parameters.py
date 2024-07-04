# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass

from core.localization.interface import _
from core.ui.input_manager import InputManager as im
from modules._base.parameters.module_parameter import ModuleParameter
from extras.warnings_manager import WarningsManager
from .filters import all_filters


@dataclass
class AudienceParserParameters:
    chats: ModuleParameter
    filter: ModuleParameter
    audience_base: ModuleParameter
    deep_parsing: ModuleParameter

    @classmethod
    def ask_user(cls) -> AudienceParserParameters:
        chats = im.get_multiline_input(_("MODULE-audience_parser-enter_chats_prompt"))
        selected_filter = im.select_from_list(
            prefix=_("MODULE-audience_parser-select_filter"),
            choices=all_filters
        )
        audience_base = im.get_raw_input(_("MODULE-audience_parser-enter_base_name"))
        deep_parsing = im.get_bool_input(_("MODULE-audience_parser-enable_deep_parsing"))
        if deep_parsing:
            WarningsManager.display_deep_parser_banner()

        return cls(
            chats=ModuleParameter(
                name=_("MODULE-audience_parser-chats"),
                value=chats
            ),
            filter=ModuleParameter(
                name=_("MODULE-audience_parser-filter"),
                value=selected_filter
            ),
            audience_base=ModuleParameter(
                name=_("MODULE-audience_parser-base"),
                value=audience_base
            ),
            deep_parsing=ModuleParameter(
                name=_("MODULE-audience_parser-deep_parsing"),
                value=deep_parsing
            )
        )
