# -*- coding: utf-8 -*-

from enum import Enum, auto


class InvitingResult(Enum):
    """For now used only for TextReportManager, so we don't need other fields"""
    OK = auto()
    PRIVACY_RESTRICTED = auto()
    OTHER = auto()
