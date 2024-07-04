# -*- coding: utf-8 -*-

from core.range import Range
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from core.localization.interface import _
from .content_factory import content_factory
from ..errors import OutOfContentError


class ContentSelector:
    """Allows the user to select between content folders"""

    @staticmethod
    def get_content_via_selector():
        """:raises OutOfContentError"""
        print()
        ui.print_header(_("MODULE-spammers-content_selector-header"))
        ui.print(_("MODULE-spammers-content_selector-hint"))
        all_content = content_factory.get_all_content()
        if not all_content:
            raise OutOfContentError
        for i, content in enumerate(all_content, start=1):
            ui.print_key_and_value(i, content.name, separator='.')
        selection_range = Range(1, len(all_content))
        selection = im.get_int_input(_("INPUT_MANAGER-int_input_prefix"), number_range=selection_range)
        content = all_content[selection - 1]
        # ui.print('[green]' + _("INPUT_MANAGER-multiline_input_done").format(len(content)) + '[/green]')
        # TODO: maybe show spintax text variants?
        return content


content_selector = ContentSelector()
