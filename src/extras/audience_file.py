# -*- coding: utf-8 -*-

from pathlib import Path
from core.utils.file_utils import FileList


class AudienceFile:
    """Represents a .txt file with audience."""

    def __init__(self, file: Path):
        self.file = FileList(filename=file)

    @property
    def audience(self) -> list[str]:
        return self.file

    def remove_user(self, user_string: str):
        return self.file.remove(user_string)
