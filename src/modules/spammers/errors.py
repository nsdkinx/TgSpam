# -*- coding: utf-8 -*-

from core.localization.interface import _


class SpammerError(Exception):
    pass


class OutOfUsersError(SpammerError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-out_of_users")
        )

class OutOfContentError(SpammerError):
    def __init__(self):
        super().__init__(
            _("MODULE-spammers-out_of_content")
        )


class TooLongFloodWaitError(SpammerError):
    def __init__(self, seconds: int):
        self.seconds = seconds
        super(Exception, self).__init__(
            _("MODULE-inviter-too_long_flood_wait").format(seconds)
        )


class AccountSpamblockedError(SpammerError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-account_spamblocked")
        )


class AccountLimitHitError(SpammerError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-account_limit_hit")
        )


class OverallLimitHitError(SpammerError):
    def __init__(self):
        super(Exception, self).__init__(
            _("MODULE-inviter-overall_limit_hit")
        )
