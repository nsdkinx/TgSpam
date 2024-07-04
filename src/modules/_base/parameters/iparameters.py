# -*- coding: utf-8 -*-

from typing import Protocol, ClassVar


class IParameters(Protocol):
    """Defines a protocol for module parameters"""

    __dataclass_fields__: ClassVar[dict]
    def ask_user(self): ...
