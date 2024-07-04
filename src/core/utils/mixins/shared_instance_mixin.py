# -*- coding: utf-8 -*-

from typing import TypeVar

T_ = TypeVar('T_')


class SharedInstanceMixin:
    _shared: T_ = None

    def __init__(self):
        if self._shared is None:
            self.__class__._shared = self

    @classmethod
    def get_shared(cls: type[T_]) -> T_:
        instance = cls._shared

        if not instance:
            raise RuntimeError(f'Shared {cls.__name__} has not been set')

        return instance
