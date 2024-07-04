# -*- coding: utf-8 -*-

from types import ModuleType
from .utils import iter_all_submodules


class ModulesRepository:
    """Finds all modules in `modules`, gets their entry points
    at `async module_main.module_main()` and the metadata from `meta`,
    then serializes them to be easily presented and then started"""

    def __init__(self, base_module: ModuleType):
        self.base_module = base_module
        self.modules = list(iter_all_submodules(base_module))

    @staticmethod
    def get_module_name(module: ModuleType) -> str:
        """Gets the module name from `modules.meta`"""
        try:
            return module.meta.MODULE_NAME
        except BaseException:
            raise RuntimeError(f'module {module} does not have meta.MODULE_NAME')

    @staticmethod
    def get_module_category(module: ModuleType) -> str:
        """Gets the module category from `modules.meta`"""
        try:
            return module.meta.MODULE_CATEGORY
        except BaseException:
            raise RuntimeError(f'module {module} does not have meta.MODULE_CATEGORY')

    def get_modules_grouped_by_category(self) -> dict[str, list[ModuleType]]:
        modules_to_return: dict[str, list[ModuleType]] = {}
        for module in self.modules:
            category = self.get_module_category(module)
            if category in modules_to_return:
                modules_to_return[category].append(module)
            else:
                modules_to_return[category] = [module]

        return modules_to_return
