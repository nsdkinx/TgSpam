# -*- coding: utf-8 -*-
import asyncio
import logging

from types import ModuleType

from core.range import Range
from core.ui.ui_manager import UIManager as ui
from core.ui.input_manager import InputManager as im
from core.localization.interface import _
from modules._base.modules_repository import ModulesRepository
from modules import _settings

logger = logging.getLogger(__name__)


class ModuleSelector:
    """Renders all software modules categorized and runs the module
    selected by user"""

    def __init__(self, modules_repository: ModulesRepository):
        self._modules_repository = modules_repository
        self._grouped_modules: dict[str, list[ModuleType]] = modules_repository.get_modules_grouped_by_category()
        self._modules_count = len(modules_repository.modules)
        self._module_index_range = Range(0, self._modules_count)
        self._module_index = 1  # To make module numbers global for all categories

    def _render_category(self, category_name: str, modules: list[ModuleType]):
        ui.print_dashed_header(category_name, inverse_colors=True)
        for module in modules:
            name = self._modules_repository.get_module_name(module)
            _module_name = module.__name__.split('.')[-1]
            ui.print_key_and_value(
                key='    ' + str(self._module_index),
                value=name,
                separator='.'
            )
            self._module_index += 1

    async def _run_module(self, module: ModuleType):
        logger.info(f'Running module {module}')
        name = module.__name__.split('.')[-1]
        return await module.module_main.module_main()

    async def select_and_run_module(self):
        ui.print_key_and_value(
            key='    0',
            value=_("MODULE-settings"),
            separator='.'
        )
        self._module_index = 1  # Reset module number index

        for category, modules in self._grouped_modules.items():
            self._render_category(category, modules)

        module_choice_index = im.get_int_input(
            _('INPUT_MANAGER-int_input_prefix'),
            number_range=self._module_index_range
        )

        if module_choice_index == 0:
            await self._run_module(_settings)
        else:
            selected_module = self._modules_repository.modules[module_choice_index-1]
            await self._run_module(selected_module)
