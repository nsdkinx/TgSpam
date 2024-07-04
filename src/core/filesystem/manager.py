# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union


class FilesystemManager:

    @staticmethod
    def create_file(file_name: Union[str, Path]) -> Path:
        path = Path(file_name)
        if not path.exists() or not path.is_file():
            path.open(mode='w', encoding='utf-8').close()
        return path

    @staticmethod
    def create_folder(folder_name: Union[str, Path]) -> Path:
        path = Path(folder_name)
        if not path.exists() or not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
        return path
