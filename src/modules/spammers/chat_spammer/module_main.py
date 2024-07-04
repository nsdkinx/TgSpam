# -*- coding: utf-8 -*-

from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _


async def module_main():
    ui.print(_("MODULE-pm_spammer-still_in_development"))
    ui.console.input(_("MODULE-base-press_enter_to_exit"))
    return
