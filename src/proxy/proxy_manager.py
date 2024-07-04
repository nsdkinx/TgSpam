# -*- coding: utf-8 -*-

from __future__ import annotations

import logging

from pathlib import Path
from core.utils.mixins.shared_instance_mixin import SharedInstanceMixin
from core.ui.ui_manager import UIManager as ui
from core.localization.interface import _

from .model import Proxy
from .software_proxy_container import SoftwareProxyContainer
from .json_proxy_manager import JsonProxyManager
from .proxy_checking_result import ProxyCheckingResult

logger = logging.getLogger(__name__)


class ProxyManager(SharedInstanceMixin):
    """High-level class for everything proxy.
    Can check proxies and serve account proxies
    (with loading them from JSON if needed)"""

    def __init__(self):
        self._software_proxy_container = SoftwareProxyContainer.get_shared()
        self._all_proxies: list[Proxy] = []

        super().__init__()

    @property
    def total_count(self):
        return len(self._all_proxies)

    def get_all_proxies(self) -> list[Proxy]:
        return self._all_proxies

    def get_proxy_for_session_file(self, session_file: Path):
        """Used in TelegramAccount loading stage to get
        a suitable proxy for an account"""
        json_file = session_file.with_suffix('.json')
        json_proxy = JsonProxyManager.get_proxy_from_json_file(json_file)
        if not json_proxy:
            software_proxy = self.get_software_proxy()
            if not software_proxy:
                logger.error(f'[{session_file}] Tried to get a proxy, it didn\'t exist in JSON file and there are no software proxies. What a world we live in')
                ui.log('[red]' + _("PROXY_MANAGER-proxy_not_found").format(str(session_file)) + '[/red]')
                return None

            JsonProxyManager.write_proxy_into_json_file(json_file, software_proxy)
            ui.log(f'[yellow]' + _("PROXY_MANAGER-replaced_proxy").format(session_file) + '[/yellow]')
            proxy_to_return = software_proxy
        else:
            proxy_to_return = json_proxy

        if proxy_to_return not in self._all_proxies:
            self._all_proxies.append(proxy_to_return)

        return proxy_to_return

    def get_software_proxy(self):
        return self._software_proxy_container.get_a_proxy()

    @staticmethod
    async def check_proxy(proxy: Proxy) -> ProxyCheckingResult:
        try:
            socket = await proxy.ps_proxy.connect(
                dest_host='149.154.167.51',
                dest_port=80,
                timeout=6
            )
            socket.close()
            return ProxyCheckingResult.ALIVE
        except BaseException as e:
            if '407' in str(e):
                return ProxyCheckingResult.INVALID_CREDENTIALS

            return ProxyCheckingResult.DEAD
