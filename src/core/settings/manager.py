# -*- coding: utf-8 -*-

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
from core.range import AnyType
from core.filesystem.helpers import is_file_empty


class SettingsManager:
    """Low level JSON file settings manager."""

    def __init__(self, settings_json_file: Path):
        self.settings_json_file = settings_json_file
        if is_file_empty(self.settings_json_file):
            self.settings_json_file.write_text('{}', encoding='utf-8')

    def _get_settings_dict(self) -> dict[str, AnyType]:
        return json.loads(self.settings_json_file.read_text(encoding='utf-8'))

    def _write_settings_dict(self, settings_dict: dict[str, AnyType]):
        self.settings_json_file.write_text(json.dumps(settings_dict, indent=4, ensure_ascii=False), encoding='utf-8')

    @contextmanager
    def edit_settings_dict(self):
        settings_dict = self._get_settings_dict()
        try:
            yield settings_dict
        finally:
            self._write_settings_dict(settings_dict)

    def get_option(self, name: str) -> Optional[AnyType]:
        return self._get_settings_dict().get(name, None)

    def set_option(self, name: str, value: AnyType):
        with self.edit_settings_dict() as settings_dict:
            settings_dict[name] = value
