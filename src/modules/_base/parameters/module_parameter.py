# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T')


@dataclass
class ModuleParameter:
    name: str
    value: T = None

    def __get__(self, instance, owner):
        return self.value
