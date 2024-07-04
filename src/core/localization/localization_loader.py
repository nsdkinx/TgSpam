# -*- coding: utf-8 -*-

from pathlib import Path
from core.localization.localization_file import LocalizationFile


class LocalizationLoader:
    """Will find .rcfg files containing META-locale_name in them"""

    def __init__(self, locales_folder: Path):
        self.locales_folder = locales_folder

        if not self.locales_folder.exists():
            raise FileNotFoundError(f'locales folder does not exist')

    def get_locales(self) -> dict[str, LocalizationFile]:
        locales: dict[str, LocalizationFile] = {}

        for file in self.locales_folder.glob('*.rcfg'):

            first_string = file.read_text('utf-8').splitlines()[0]
            first_string_key, locale_name = first_string.split(': ')

            if first_string_key == 'META-locale_name':
                locales[locale_name] = LocalizationFile(file)

        return locales
