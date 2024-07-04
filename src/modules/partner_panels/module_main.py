# -*- coding: utf-8 -*-

from core.range import Range
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from core.localization.interface import _
from .partner_panel import PartnerPanel


PARTNER_PANELS = [
    PartnerPanel(name='TeaTeaGram', referral_link='https://teateagram.com/ref176244'),
    PartnerPanel(name='Targetlike', referral_link='https://targetlike.com/ref329399')
]


async def module_main():
    ui.paginate(_("MODULE-partner_panels"))
    ui.print(_("MODULE-partner_panels-banner"))
    ui.print_key_and_value(0, _("SETTINGS-back_to_menu"))
    for i, partner_proxy in enumerate(PARTNER_PANELS, start=1):
        ui.print_key_and_value(i, partner_proxy.name, separator='.')
    print()

    selection_range = Range(0, len(PARTNER_PANELS))
    selection = im.get_int_input(_("MODULE-partner_panels-select_panel"), number_range=selection_range)

    if selection == 0:
        return

    selected_partner_panel = PARTNER_PANELS[selection - 1]
    selected_partner_panel.open_referral_link_in_browser()

    return
