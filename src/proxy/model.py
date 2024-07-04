# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal
from python_socks.async_.asyncio import ProxyType, Proxy as PSProxy, HttpProxy, Socks5Proxy


@dataclass
class Proxy:
    proxy_type: Literal['socks5', 'http'] | None
    addr: str
    port: int
    username: str | None = None
    password: str | None = None
    rdns: bool = True

    @property
    def telethon(self) -> dict:
        return asdict(self)

    @property
    def ps_proxy_type(self):
        if self.proxy_type == 'http':
            return ProxyType.HTTP
        elif self.proxy_type == 'socks5':
            return ProxyType.SOCKS5
        else:
            raise RuntimeError(f'Proxy type is {self.proxy_type}')

    @property
    def ps_proxy(self) -> HttpProxy | Socks5Proxy:
        return PSProxy.create(
            proxy_type=self.ps_proxy_type,
            host=self.addr,
            port=self.port,
            username=self.username,
            password=self.password,
            rdns=self.rdns
        )
