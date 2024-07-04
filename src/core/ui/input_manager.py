# -*- coding: utf-8 -*-

import asyncio
from typing import Union
from rich.console import Console
from .config import accent_color
from ..range import Range
from .ui_manager import UIManager as ui
from core.localization.interface import _
from core.app_exit_routine import AppExitRoutine
from core.utils.telethon_utils import adapt_link


class InputManager:
    """Gets the input from user, validates and prettifies it"""
    console = Console(highlight=False)

    @classmethod
    def get_raw_input(cls, prefix: str, must_be_not_none: bool = True) -> str:
        """Unvalidated raw string input"""
        _did_press_ctrl_c: bool = False
        while True:
            try:
                input_data = cls.console.input(f'{prefix} [{accent_color}]>>[/] ')
                if input_data in ['', ' ', '\n'] and must_be_not_none:
                    ui.print(_("INPUT_MANAGER-input_none"))
                    return cls.get_raw_input(prefix, must_be_not_none)
                return input_data
            except (KeyboardInterrupt, EOFError):
                if _did_press_ctrl_c:
                    AppExitRoutine.exit_app_sync()
                    return

                cls.console.print('\n' + _('INPUT_MANAGER-keyboard_interrupt_msg'))
                _did_press_ctrl_c = True
                continue

    @classmethod
    def get_username_input(cls, prefix: str) -> str:
        raw_input = cls.get_raw_input(prefix, must_be_not_none=True)
        return adapt_link(raw_input)

    @classmethod
    def get_int_input(cls, prefix: str, number_range: Range = None) -> int:
        """Get an integer from user, optionally -- in the specified range"""
        while True:
            _input = cls.get_raw_input(prefix)
            if not _input.isdigit():
                cls.console.print(_('INPUT_MANAGER-must_be_int'))
                continue
            if not number_range:
                return int(_input)
            if not number_range.is_number_in_range(int(_input)):
                cls.console.print(_("INPUT_MANAGER-must_be_in_range"))
                continue
            return int(_input)

    @classmethod
    def get_bool_input(cls, prefix: str) -> bool:
        """Ask yes or no"""
        cls.console.print(f'[bold {accent_color}]{prefix}[/]')
        cls.console.print(f'[{accent_color}]1.[/] {_("yes")}')
        cls.console.print(f'[{accent_color}]2.[/] {_("no")}')
        choice = cls.get_int_input(prefix=_("INPUT_MANAGER-bool_choice_prefix"), number_range=Range(1, 2))

        if choice == 1:
            return True
        elif choice == 2:
            return False

    @classmethod
    def select_from_list(cls, prefix: str, choices: list[str], return_index: bool = False) -> Union[str, int]:
        """Ask the user to choose an item in the list.
        :param prefix: prefix
        :param choices: list of choices
        :param return_index: return an index of the item in the list instead of the item content"""
        total_choices = len(choices)

        cls.console.print(ui.make_accented_text(prefix, bold=True))
        for i, choice in enumerate(choices, start=1):
            cls.console.print(f'[{accent_color}]{i}.[/] {choice}')

        while True:
            choice_index = cls.get_int_input(_("INPUT_MANAGER-int_input_prefix"))
            if choice_index > total_choices:
                cls.console.print(_("INPUT_MANAGER-no_such_variant"))
                continue
            break

        if return_index:
            return choice_index
        else:
            return choices[choice_index - 1]

    @classmethod
    def get_range_input(cls, prefix: str) -> str:
        """A text string representing a range (e.g. 3-5).
        Can then be converted into Range"""
        while True:
            value = cls.get_raw_input(prefix, must_be_not_none=True)
            if '-' not in value and not value.isdigit():
                continue
            if '-' not in value and value.isdigit():
                return value
            _split = value.split('-')
            if len(_split) != 2:
                continue
            if not all([_split[0].isdigit(), _split[1].isdigit()]):
                continue
            return value

    @classmethod
    def get_multiline_input(cls, prefix: str) -> list[str]:
        """Ask user to enter a multiline text. For example, to load groups list"""
        ui.print(f'[bold #000000 on {accent_color}] + [/] {prefix}')
        lines: list[str] = []
        while True:
            try:
                line = cls.console.input()
                if line in ['', ' ', '\n']:
                    break
                lines.append(line)
            except EOFError:
                break

        if not lines:
            ui.print(_("INPUT_MANAGER-multiline_input_none"))
            return cls.get_multiline_input(prefix)

        ui.print('[green]' + _("INPUT_MANAGER-multiline_input_done").format(len(lines)) + '[/green]')
        return lines
