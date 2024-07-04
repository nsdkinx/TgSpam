# -*- coding: utf-8 -*-

class PMSpammerStatistics:
    successful_sends: int = 0
    not_found: int = 0

    @classmethod
    def get_total_send_attempts(cls):
        return cls.successful_sends \
            + cls.not_found

    @classmethod
    def clear(cls):
        cls.successful_sends: int = 0
        cls.not_found: int = 0
