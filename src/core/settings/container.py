# -*- coding: utf-8 -*-

import logging
from core.settings.models import SettingsOption
from core.settings.option_type import (
    OptionTypeEnum,
    OptionTypeInt,
    OptionTypeBool,
    OptionTypeRange
)
from core.localization.interface import _

logger = logging.getLogger(__name__)


class SettingsContainer:
    proxy_type = SettingsOption(
        name=_("SETTINGS-proxy_type"),
        description=_("SETTINGS-proxy_type-description"),
        category=_("SETTINGS-category-general"),
        default_value='http',
        type=OptionTypeEnum('socks5', 'http')
    )
    concurrency_limit = SettingsOption(
        name=_("SETTINGS-concurrency_limit"),
        description=_("SETTINGS-concurrency_limit-description"),
        category=_("SETTINGS-category-general"),
        default_value=10,
        type=OptionTypeInt()
    )
    check_proxy_before_work = SettingsOption(
        name=_("SETTINGS-check_proxy_before_work"),
        description=_("SETTINGS-check_proxy_before_work-description"),
        category=_("SETTINGS-category-general"),
        default_value=True,
        type=OptionTypeBool()
    )
    sort_accounts_to_folders = SettingsOption(
        name=_("SETTINGS-sort_accounts_to_folders"),
        description=_("SETTINGS-sort_accounts_to_folders-description"),
        category=_("SETTINGS-category-general"),
        default_value=True,
        type=OptionTypeBool()
    )
    thread_start_delay = SettingsOption(
        name=_("SETTINGS-thread_start_delay"),
        description=_("SETTINGS-thread_start_delay-description"),
        category=_("SETTINGS-category-general"),
        default_value='10-15',
        type=OptionTypeRange()
    )
    peer_flood_limit = SettingsOption(
        name=_("SETTINGS-peer_flood_limit"),
        description=_("SETTINGS-peer_flood_limit-description"),
        category=_("SETTINGS-category-inviter"),
        default_value=5,
        type=OptionTypeInt()
    )

    def get_all_options(self) -> list[SettingsOption]:
        to_return = [
            option
            for attribute_name, option in vars(self.__class__).items()
            if not attribute_name.endswith('__')
            and not callable(option)
        ]
        formatted_settings_options = [repr(option) for option in to_return]
        formatted_options = '[\n' + ',\n    '.join(formatted_settings_options) + '\n]'
        logger.info(f'SettingsContainer.get_all_options() => {formatted_options}')
        return to_return


settings = SettingsContainer()
