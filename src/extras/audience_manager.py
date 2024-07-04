# -*- coding: utf-8 -*-

from pathlib import Path
from .audience_file import AudienceFile


class AudienceManager:
    """Manages the .txt files of collected audience
    in the specified folder"""

    def __init__(self, folder: Path):
        self.folder = folder

    def iter_audience_bases(self):
        for file in self.folder.glob('*.txt'):
            yield AudienceFile(file=file)

    @property
    def total_bases_amount(self):
        return len(list(self.folder.glob('*.txt')))
