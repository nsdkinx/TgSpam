# -*- coding: utf-8 -*-

from core.localization.interface import _


class InviterError(Exception):
    pass


class NoAudienceBasesError(InviterError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-no_audience_bases")
        )


class ChatNotFoundError(InviterError):
    def __init__(self, chat: str):
        self.chat = chat
        super(Exception, self).__init__(
            _("MODULE-inviter-chat_not_found").format(chat)
        )


class OutOfUsersError(InviterError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-out_of_users")
        )


class TooLongFloodWaitError(InviterError):
    def __init__(self, seconds: int):
        self.seconds = seconds
        super(Exception, self).__init__(
            _("MODULE-inviter-too_long_flood_wait").format(seconds)
        )


class AccountSpamblockedError(InviterError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-account_spamblocked")
        )


class AccountLimitHitError(InviterError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-account_limit_hit")
        )


class OverallLimitHitError(InviterError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-overall_limit_hit")
        )
