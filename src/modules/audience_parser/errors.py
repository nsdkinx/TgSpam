# -*- coding: utf-8 -*-

from core.localization.interface import _


class ParserError(Exception):
    pass


class ChatNotFoundError(ParserError):
    def __init__(self):
        super().__init__(_("MODULE-audience_parser-chat_not_found"))


class NeedsAdminError(ParserError):
    def __init__(self):
        super().__init__(_("MODULE-audience_parser-chat_admin_required"))
