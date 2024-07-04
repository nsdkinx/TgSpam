# -*- coding: utf-8 -*-

from functools import cached_property, cache
from pathlib import Path


class LocalizationFile:
    """Represents a .rcfg file with locales"""

    def __init__(self, file_path: Path):
        self.file_path = file_path

        if not file_path.exists():
            raise FileNotFoundError(f'Localization file `{file_path}` does not exist!')

    @cache
    def __repr__(self):
        return f'LocalizationFile(file_path={self.file_path})'

    def __hash__(self):
        return hash(self.file_path)

    @cached_property
    def locale_file_name(self):
        return self.file_path.name.removesuffix('.rcfg')

    def deserialize_into_dict(self) -> dict[str, str]:
        result_dict: dict[str, str] = {}
        
        file_lines = self.file_path.read_text('utf-8').splitlines()
        
        for line in file_lines:
            if (not line.strip()) or line.startswith('//'):
                continue
            
            key, value = line.split(': ')
            result_dict[key] = value
        
        return result_dict
