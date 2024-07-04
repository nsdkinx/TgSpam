# -*- coding: utf-8 -*-

from enum import Enum, auto


class SpamblockCheckingResult(Enum):
    NO_SPAMBLOCK = auto()
    TEMPORARY_SPAMBLOCK = auto()
    ETERNAL_SPAMLBOCK = auto()
