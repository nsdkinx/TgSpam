# -*- coding: utf-8 -*-

from abc import ABC, ABCMeta, abstractmethod
from datetime import timedelta, datetime

from telethon.tl import types
from core.localization.interface import _


class BaseFilterMeta(ABCMeta):
    def __repr__(cls):
        return cls.filter_name  # noqa


class BaseFilter(ABC, metaclass=BaseFilterMeta):
    filter_name: str

    @staticmethod
    def _do_base_filtering(user: types.User):
        if user.bot:
            return False
        if not user.username:
            return False
        return True

    @abstractmethod
    def validate_user(self, user: types.User):
        raise NotImplementedError


class AllMembersFilter(BaseFilter):
    filter_name = _("MODULE-audience_parser-filter-all_members")

    def validate_user(self, user: types.User):
        if not self._do_base_filtering(user):
            return False
        return True


class RecentlyOnlineFilter(BaseFilter):
    filter_name = _("MODULE-audience_parser-filter-recently_online")

    def validate_user(self, user: types.User):
        if not self._do_base_filtering(user):
            return False
        if isinstance(user.status, types.UserStatusOffline):
            _tzinfo = user.status.was_online.tzinfo
            delta: timedelta = datetime.now(_tzinfo) - user.status.was_online
            if delta.days <= 3:
                return True
            else:
                return False
        elif isinstance(user.status, types.UserStatusOnline):
            return True
        elif isinstance(user.status, types.UserStatusRecently):
            return True
        else:
            return False


class InactiveFilter(BaseFilter):
    filter_name = _("MODULE-audience_parser-filter-inactive")

    def validate_user(self, user: types.User):
        if not self._do_base_filtering(user):
            return False
        if isinstance(user.status, types.UserStatusOffline):
            _tzinfo = user.status.was_online.tzinfo
            delta: timedelta = datetime.now(_tzinfo) - user.status.was_online
            if delta.days >= 10:
                return True
            else:
                return False
        elif isinstance(user.status, types.UserStatusOnline):
            return False
        elif isinstance(user.status, types.UserStatusRecently):
            return False
        else:
            return True


class PremiumOnlyFilter(BaseFilter):
    filter_name = _("MODULE-audience_parser-filter-premium_only")

    def validate_user(self, user: types.User):
        if not self._do_base_filtering(user):
            return False
        if user.premium:
            return True
        else:
            return False


all_filters = [
    AllMembersFilter,
    RecentlyOnlineFilter,
    InactiveFilter,
    PremiumOnlyFilter
]
