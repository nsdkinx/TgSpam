# -*- coding: utf-8 -*-

from enum import Enum, auto
from core.localization.interface import _


class AccountCheckingResult(Enum):
    ALIVE = _('MODULE-account_checker-results-alive')
    CONNECTION_ERROR = _('MODULE-account_checker-results-connection_error')
    DEAD_AFTER_CONNECTING = _('MODULE-account_checker-results-dead_after_connecting')
    RESET_ALL_SESSIONS = _('MODULE-account_checker-results-reset_all_sessions')
    TEMPORARY_SPAMBLOCK = _('MODULE-account_checker-results-temporary_spamblock')
    ETERNAL_SPAMBLOCK = _('MODULE-account_checker-results-eternal_spamblock')
    AUTH_KEY_DUPLICATED = _('MODULE-account_checker-results-auth_key_duplicated')
    AUTH_KEY_UNREGISTERED = _('MODULE-account_checker-results-auth_key_unregistered')
    DEACTIVATED = _('MODULE-account_checker-results-deactivated')
    PHONE_NUMBER_BANNED = _('MODULE-account_checker-results-phone_number_banned')
    OTHER_ERROR = _('MODULE-account_checker-results-other_error')
