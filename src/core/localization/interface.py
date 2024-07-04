# -*- coding: utf-8 -*-

import logging
from typing import Callable

from .localization_loader import LocalizationLoader
from .localizator import Localizator
from .selected_locale_storage import SelectedLocaleStorage
from .config import LOCALES_FOLDER, SELECTED_LOCALE_FILE

localization_loader = LocalizationLoader(LOCALES_FOLDER)
selected_locale_storage = SelectedLocaleStorage(localization_loader, SELECTED_LOCALE_FILE)

logger = logging.getLogger(__name__)


def get_translation_function() -> Callable[[str], str]:
    """Highest level interface for localization.
    Will return a callable object to translate strings."""

    current_localization_file = selected_locale_storage.get_current_locale()
    if current_localization_file:
        localizator = Localizator(current_localization_file)
        logger.info(f"Loading already selected locale '{current_localization_file.locale_file_name}'")
        return localizator.translate

    print('Select your language:')
    available_locales = localization_loader.get_locales()
    for i, locale_data in enumerate(available_locales.items(), start=1):
        print(f'    {i}. {locale_data[0]}')

    while True:
        index = input('> ')
        if not index.isdigit():
            continue
        index = int(index)
        try:
            current_localization_file = list(available_locales.values())[index - 1]
        except IndexError:
            continue
        break

    logger.info(f"Loading new locale '{current_localization_file.locale_file_name}'")
    selected_locale_storage.set_locale(current_localization_file)
    localizator = Localizator(current_localization_file)

    return localizator.translate


_ = get_translation_function()
