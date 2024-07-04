# -*- coding: utf-8 -*-

import inspect
from types import ModuleType
from typing import Generator


def iter_all_submodules(module: ModuleType) -> Generator[ModuleType, None, None]:
    _vars = vars(module)
    for module in _vars.items():
        if (
                not module[0].endswith('__')
                and inspect.ismodule(module[1])
                # and not hasattr(module[1], 'MR_IGNORE')
                and not module[0].startswith('_')
        ):
            yield module[1]
