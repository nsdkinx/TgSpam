# -*- coding: utf-8 -*-

from pathlib import Path
from ..randomizable_text import RandomizableText


class Content:
    """Represents single message content"""

    def __init__(self, name: str, texts: list[RandomizableText], media: list[Path]):
        self.name = name
        self.texts = texts
        self.media = media

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
