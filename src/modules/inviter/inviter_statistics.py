# -*- coding: utf-8 -*-

class InviterStatistics:
    successful_invites: int = 0
    privacy_restricted: int = 0
    not_found: int = 0
    too_many_channels: int = 0
    instantly_removed: int = 0

    @classmethod
    def get_total_inviting_attempts(cls):
        return cls.successful_invites \
            + cls.privacy_restricted \
            + cls.not_found \
            + cls.too_many_channels \
            + cls.instantly_removed

    @classmethod
    def get_successful_invites(cls):
        """hack to get more accurate statistics"""
        return cls.get_total_inviting_attempts() \
            - cls.get_unable_to_invite()

    @classmethod
    def get_unable_to_invite(cls):
        return cls.privacy_restricted \
            + cls.not_found \
            + cls.too_many_channels \
            + cls.instantly_removed

    @classmethod
    def clear(cls):
        cls.successful_invites: int = 0
        cls.privacy_restricted: int = 0
        cls.not_found: int = 0
        cls.too_many_channels: int = 0
        cls.instantly_removed: int = 0
