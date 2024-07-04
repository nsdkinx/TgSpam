# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional

from .localization_file import LocalizationFile
from .localization_loader import LocalizationLoader
from ..filesystem.helpers import is_file_empty


class SelectedLocaleStorage:
    """We need special storage for the current localization choice
    because it operates on such a low level that even the default
    settings storage must be covered by it.
    It's a file contained in `data` which contains the current
    localization file name."""

    def __init__(
            self,
            localization_loader: LocalizationLoader,
            storage_file_name: Path
    ):
        self.localization_loader = localization_loader

        self.storage_file_name = storage_file_name
        if not self.storage_file_name.exists():
            self.storage_file_name.touch(exist_ok=True)

        self._locales = self.localization_loader.get_locales()

    def get_current_locale(self) -> Optional[LocalizationFile]:
        if is_file_empty(self.storage_file_name):
            return None

        locale_file_name = self.storage_file_name.read_text('utf-8').strip()

        selected_localization_file = [
            file for file in self._locales.values() if file.locale_file_name == locale_file_name
        ]

        if len(selected_localization_file) != 1:
            raise RuntimeError(f'unable to get current locale: there are none or too many locales')

        return selected_localization_file[0]

    def set_locale(self, locale: LocalizationFile) -> None:
        self.storage_file_name.write_text(locale.locale_file_name, encoding='utf-8')
