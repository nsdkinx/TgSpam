# -*- coding: utf-8 -*-

from dataclasses import dataclass
from core.range import AnyType
from core.filesystem.container import files
from .manager import SettingsManager
from .option_type import BaseOptionType

settings_manager = SettingsManager(files.settings_file)


@dataclass
class SettingsOption:
    name: str
    description: str
    category: str
    default_value: AnyType
    type: BaseOptionType

    _value: AnyType = None

    def __post_init__(self):
        """Will create the option in settings when the instance of it is created."""
        value = settings_manager.get_option(self.name)
        if value == None:  # noqa
            settings_manager.set_option(self.name, self.default_value)
            value = self.default_value
            self._value = value
            return

        self._value = value

    def __get__(self, instance, owner):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: AnyType):
        """Sets the option"""
        settings_manager.set_option(self.name, value)
        self._value = value
