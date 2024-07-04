# -*- coding: utf-8 -*-

import os
from typing import Sized, Union
from collections.abc import Iterable

from rich.console import Console
from contextlib import contextmanager
from datetime import datetime
from .config import accent_color
from core.localization.interface import _  # noqa


class UIManager:
    """Prints things like accent-colored headers, grouped selectors, info tables,
    logs with time, etc"""
    console = Console(highlight=False)

    @classmethod
    def print_dashed_header(cls, header_text: str, inverse_colors: bool = False):
        """Prints a header like this:
        --- Program activation ---"""
        if not inverse_colors:
            return cls.console.print(f"{cls.make_accented_text('---')} {header_text} {cls.make_accented_text('---')}")
        else:
            return cls.console.print(f"--- {cls.make_accented_text(header_text)} ---")

    @classmethod
    @contextmanager
    def wrap_with_header(cls, header_text: str):
        """Wraps some actions with a header like this:
        --- Program activation ---
        Enter your license key >>> amogus
        - 23:58:33 - Program activated!
        --- ------ ----------- ---

        with ui_manager.wrap_with_header('Program activation'):
            input_manager.raw_input('Enter your license key')
            ui_manager.log('Program activated!')"""
        dashed_header = ''.join(['-' if c != ' ' else c for c in header_text])
        cls.print_dashed_header(header_text)
        try:
            yield
        finally:
            cls.print_dashed_header(dashed_header)

    @classmethod
    def log(cls, text: str):
        """Logs a message with dimmed time in the beginning"""
        return cls.console.print(f"[dim]- {datetime.now().strftime('%H:%M:%S')} -[/dim] {text}")

    @classmethod
    def print(cls, text: str):
        """Print. Just print."""
        return cls.console.print(text)

    @classmethod
    def print_header(cls, text: str):
        """Prints a simple bold text header"""
        return cls.console.print(cls.make_accented_text(text, bold=True))

    @classmethod
    def make_accented_text(cls, text: Union[str, int], bold: bool = False, highlight_zero: bool = False):
        if (text == '0' or text == 0) and highlight_zero:
            return f"[{'bold ' if bold else ''}red]" \
                   f"{text} (!!)" \
                   f"[/{'bold ' if bold else ''}red]"
        return f"[{'bold ' if bold else ''}{accent_color}]" \
               f"{text}" \
               f"[/{'bold ' if bold else ''}{accent_color}]"

    @classmethod
    def translate_bool(cls, raw_value: Union[str, int, bool]) -> str:
        """Pretty prints the option value.
        For example, turning boolean values into colored text"""
        if isinstance(raw_value, bool):
            if raw_value:
                return f'[bold green]{_("yes")}[/]'
            else:
                return f'[bold red]{_("no")}[/]'
        else:
            return raw_value

    @classmethod
    def translate_iterable(cls, iterable: Union[Iterable, Sized]) -> str:
        """Turns an iterable (list/tuple/set) into a pretty-printed string"""
        if len(iterable) <= 3:
            return cls.make_accented_text(', '.join(iterable))
        else:
            return cls.make_accented_text(_(f'UI_MANAGER-elements').format(len(iterable)))

    @classmethod
    def print_key_and_value(
            cls,
            key: Union[str, int],
            value: Union[str, int],
            *,
            separator: str = ':',
            inverse_colors: bool = False,
            add_tabulation: bool = False
    ):
        def make_first_part():
            if inverse_colors:
                return key + separator
            return cls.make_accented_text(key) + separator

        def make_second_part():
            if isinstance(value, bool):
                return cls.translate_bool(value)
            if isinstance(value, Iterable) and not isinstance(value, str):
                return cls.translate_iterable(value)
            if inverse_colors:
                return cls.make_accented_text(value if value else cls.translate_bool(False))
            # cls.translate_bool(False) is used to make it red colored
            return value if value else cls.translate_bool(False)

        if not add_tabulation:
            return cls.console.print(
                f'{make_first_part()} {make_second_part()}'
            )
        else:
            return cls.console.print(
                f'    {cls.make_accented_text("-") if not inverse_colors else "-"} '
                f'{make_first_part()} '
                f'{make_second_part()}'
            )

    @classmethod
    def clear(cls):
        """Clears the console and fixes the overlapping text bug"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @classmethod
    def paginate(cls, header_text: str):
        """Clears the console and prints the header.
        I'm not using Rich's pagination technologies
        cuz it makes the architecture more complex"""
        cls.clear()
        cls.print_dashed_header(header_text, inverse_colors=True)
        print()

    @classmethod
    def set_window_title(cls, title: str):
        """Sets the window title"""
        return cls.console.set_window_title(title)
