# -*- coding: utf-8 -*-

from core.range import Range
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from core.localization.interface import _

from . import pm_spammer, chat_spammer


async def module_main():
    ui.print_header(_("MODULE-spammers-header"))
    ui.print_key_and_value(0, _("SETTINGS-back_to_menu"))
    ui.print_key_and_value(1, _("MODULE-pm_spammer"))
    ui.print_key_and_value(2, _("MODULE-chat_spammer"))
    selection_range = Range(0, 2)
    selection = im.get_int_input(_("INPUT_MANAGER-int_input_prefix"), number_range=selection_range)
    if selection == 0:
        return
    elif selection == 1:
        return await pm_spammer.module_main.module_main()
    elif selection == 2:
        return await chat_spammer.module_main.module_main()
