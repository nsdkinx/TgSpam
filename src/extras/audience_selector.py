# -*- coding: utf-8 -*-

from core.range import Range
from extras.audience_manager import AudienceManager
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from core.localization.interface import _
from modules.inviter.errors import NoAudienceBasesError


class AudienceSelector:
    """Allows the user to select between audience bases or write
    the audience manually"""

    def __init__(self, audience_manager: AudienceManager):
        self.audience_manager = audience_manager

    def get_audience_base_via_selector(self):
        print()
        ui.print_header(_("EXTRAS-audience_selector-header"))
        ui.print(_("EXTRAS-audience_selector-audience_base_hint"))
        if not self.audience_manager.total_bases_amount:
            raise NoAudienceBasesError
        for i, audience_base in enumerate(self.audience_manager.iter_audience_bases(), start=1):
            ui.print_key_and_value(i, audience_base.file.filename.name, separator='.')
        selection_range = Range(1, self.audience_manager.total_bases_amount)
        selection = im.get_int_input(_("INPUT_MANAGER-int_input_prefix"), number_range=selection_range)
        audience = list(self.audience_manager.iter_audience_bases())[selection - 1].audience
        ui.print('[green]' + _("INPUT_MANAGER-multiline_input_done").format(len(audience)) + '[/green]')
        print()
        return audience
