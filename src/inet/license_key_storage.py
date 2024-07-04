# -*- coding: utf-8 -*-

import logging
from pathlib import Path
from core.ui.input_manager import InputManager as im
from core.localization.interface import _

logger = logging.getLogger(__name__)


class LicenseKeyStorage:

    def __init__(self, file: Path):
        self.file = file
        if not file.exists():
            logger.info(f'{file} does not exist, creating')
            file.touch()

    @staticmethod
    def _remove_commented_lines(text: str) -> str:
        lines = text.splitlines()
        new_lines: list[str] = []
        for line in lines:
            if line.startswith('// '):
                continue
            new_lines.append(line)
        return '\n'.join(new_lines)

    def read_key(self):
        data = self.file.read_text('utf-8').strip()
        data = self._remove_commented_lines(data)
        if not data:
            logger.info(f'License key file is empty ({data}), so asking user')
            return im.get_raw_input(_("ONBOARDING-enter_license_key")).strip()
        logger.info(f'Reading key `{data}`')
        return data

    def write_key(self, key: str):
        logger.info(f'Writing key `{key}`')
        return self.file.write_text(key, encoding='utf-8')
