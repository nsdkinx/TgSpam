# -*- coding: utf-8 -*-

from core.localization.interface import _


class ContentError(Exception):
    pass


class NoTextsError(ContentError):
    def __init__(self) -> None:
        super().__init__(_("MODULE-spammers-no_texts_error"))
