# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Union
from random import uniform

AnyType = Union[str, int, bool]


class Range:
    """A custom range class that allows to make a number range
    from a text string and do various stuff with it."""

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    @classmethod
    def make_from_text_string(cls, string: str) -> Range:
        if string.isdigit():
            return Range(int(string), int(string))
        start, end = string.split('-')
        return Range(int(start), int(end))

    def is_number_in_range(self, number: int) -> bool:
        if self.start == self.end and number == self.start:
            return True
        return self.start <= number <= self.end

    def make_random_number(self) -> float:
        if self.start == self.end:
            return self.start
        return round(uniform(self.start, self.end), 2)
