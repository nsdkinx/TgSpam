# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from core.range import Range, AnyType
from core.ui.input_manager import InputManager as im
from core.localization.interface import _


class BaseOptionType(ABC):

    @abstractmethod
    def validate(self, value: AnyType) -> bool:
        raise NotImplementedError

    @abstractmethod
    def ask_value_from_user(self):
        return im.get_int_input(_("MODULE-settings-set_int_prefix"))


class OptionTypeEnum(BaseOptionType):

    def __init__(self, *args):
        self.items = list(args)

    def validate(self, value: AnyType):
        if value not in self.items:
            return False
        return True

    def ask_value_from_user(self):
        return im.select_from_list(_("MODULE-settings-set_prefix"), self.items)


class OptionTypeInt(BaseOptionType):

    def __init__(self, number_range: Range = None):
        self.number_range = number_range

    def validate(self, value: AnyType):
        if not isinstance(value, int):
            return False
        if self.number_range:
            if not self.number_range.is_number_in_range(value):
                return False

        return True

    def ask_value_from_user(self):
        return im.get_int_input(_("MODULE-settings-set_int_prefix"), self.number_range)


class OptionTypeBool(BaseOptionType):

    def validate(self, value: AnyType):
        if not isinstance(value, bool):
            return False
        else:
            return True

    def ask_value_from_user(self):
        return im.get_bool_input(_("MODULE-settings-set_prefix"))


class OptionTypeRange(BaseOptionType):

    def validate(self, value: AnyType) -> bool:
        if not isinstance(value, str):
            return False
        if '-' not in value and not value.isdigit():
            return False
        if '-' not in value and value.isdigit():
            return True
        _split = value.split('-')
        if len(_split) != 2:
            return False
        if not all([_split[0].isdigit(), _split[1].isdigit()]):
            return False
        return True

    def ask_value_from_user(self):
        return im.get_range_input(_('INPUT_MANAGER-range_choice_prefix'))
