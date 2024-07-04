# -*- coding: utf-8 -*-

from .spintax import spin


class RandomizableText:
    """Represents a spintax randomizable text object."""

    def __init__(self, name: str, base_text: str):
        self._name = name
        self._base_text = base_text

    @property
    def name(self):
        return self._name

    def get_text(self) -> str:
        """Returns a randomized variant of the base text"""
        return spin(self._base_text)
