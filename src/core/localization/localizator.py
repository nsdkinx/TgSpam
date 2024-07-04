# -*- coding: utf-8 -*-

from __future__ import annotations

import logging

from core.localization.localization_file import LocalizationFile
from core.utils.mixins.shared_instance_mixin import SharedInstanceMixin
from core.utils import DEBUG_MODE

logger = logging.getLogger(__name__)


class Localizator(SharedInstanceMixin):
    def __init__(self, localization_file: LocalizationFile):
        self.localization_file = localization_file
        logger.debug(f'Localization file: {self.localization_file}')

        self.strings: dict[str, str] = self.localization_file.deserialize_into_dict()
        logger.debug(f'Loaded {len(self.strings.keys())} strings')

        super().__init__()

    def translate(self, string: str) -> str:
        """Translate a given string"""
        try:
            return self.strings[string]
        except KeyError:
            logger.info(f'Unlocalized string in {self.localization_file}: "{string}"')
            return string
