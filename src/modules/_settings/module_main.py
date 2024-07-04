# -*- coding: utf-8 -*-

import os
from core.settings.container import settings
from core.settings.models import SettingsOption
from core.range import Range
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from core.localization.interface import _
from core.filesystem.container import files


class SettingsUI:
    """User interface for software settings."""

    @classmethod
    def _print_option(cls, i: int, option: SettingsOption):
        ui.print(
            f'\[{i}] [bold dim]\[{option.category.center(15)}][/bold dim] {option.name}: '
            f'{ui.translate_bool(option.value)}'
        )

    @classmethod
    def ask_and_set_option(cls, option: SettingsOption):
        new_value = option.type.ask_value_from_user()
        option.value = new_value

    @classmethod
    async def start(cls):
        """Start the UI loop"""
        while True:
            ui.paginate(_("MODULE-settings"))

            options = settings.get_all_options()
            options_count = len(options)

            ui.print(
                f'\[0] {_("SETTINGS-back_to_menu")}'
            )

            for i, option in enumerate(options, start=1):
                cls._print_option(i, option)

            ui.print(
                f'\[{options_count+1}] {_("SETTINGS-open_accounts_folder")}'
            )
            ui.print(
                f'\[{options_count+2}] {_("SETTINGS-open_proxy_file")}'
            )

            print()
            option_index = im.get_int_input(_("INPUT_MANAGER-int_input_prefix"), number_range=Range(0, options_count+2))

            if option_index == 0:
                break
            elif option_index == options_count+1:
                os.system(f'explorer {str(files.accounts_folder.absolute())}')
                continue
            elif option_index == options_count+2:
                ui.print(_("UI-restart_to_apply"))
                os.system(f'notepad {str(files.proxy_file.absolute())}')
                continue

            selected_option = options[option_index-1]
            print()
            ui.print(f'[bold]{selected_option.name}[/]')
            print(selected_option.description)
            print()
            cls.ask_and_set_option(selected_option)


async def module_main():
    await SettingsUI.start()
