# -*- coding: utf-8 -*-

from __future__ import annotations

import itertools
import logging
from pathlib import Path

from core.utils.mixins.shared_instance_mixin import SharedInstanceMixin
from .model import Proxy
from core.settings.container import settings
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _
from .proxy_formats import (
    convert_regular_proxy,
    convert_regular_proxy_with_protocol,
    convert_at_symbol_proxy,
    convert_at_symbol_proxy_with_protocol
)
from .exceptions import ProxyInvalidError

logger = logging.getLogger(__name__)


class SoftwareProxyContainer(SharedInstanceMixin):
    """Contains the proxies loaded into the software"""

    def __init__(self, proxies: list[Proxy]):
        self.proxies = proxies
        self._cyclic_proxy_iterator = itertools.cycle(proxies)

        super().__init__()

    @staticmethod
    def _convert_string_into_model(string: str):
        if '://' not in string and '@' not in string:
            return convert_regular_proxy(string)
        if '://' in string and '@' not in string:
            return convert_regular_proxy_with_protocol(string)
        if '://' not in string and '@' in string:
            return convert_at_symbol_proxy(string)
        if '://' in string and '@' in string:
            return convert_at_symbol_proxy_with_protocol(string)

        raise ProxyInvalidError('unable to detect proxy type')

    @classmethod
    def make_from_file(cls, file: Path):
        proxy_lines = file.read_text('utf-8').splitlines()
        proxies = []
        for proxy_line in proxy_lines:
            try:
                proxy = cls._convert_string_into_model(proxy_line)
            except BaseException as e:
                logger.exception('Error while converting a proxy (in make_from_file).')
                ui.log('[red]' + _("PROXY-invalid_proxy_while_loading").format(proxy_line) + '[/red]')
                continue
            if not proxy.proxy_type:
                proxy.proxy_type = settings.proxy_type
            proxies.append(proxy)

        return cls(proxies)

    @property
    def total_count(self):
        return len(self.proxies)

    def get_a_proxy(self) -> Proxy | None:
        """Returns one of the proxies loaded into the software
        or None if there are none"""
        try:
            return next(self._cyclic_proxy_iterator)
        except StopIteration:
            return None
