# -*- coding: utf-8 -*-

from .model import Proxy
from .exceptions import ProxyInvalidError
from core.stability_utils import expects


def convert_at_symbol_proxy(proxy_string: str) -> Proxy:
    """user:pass@ip:port"""
    _split_by_at_symbol: list[str] = proxy_string.split('@')
    expects(
        len(_split_by_at_symbol) == 2,
        callback=ProxyInvalidError('_split_by_at_symbol != 2')
    )
    username_password, addr_port = _split_by_at_symbol
    addr, port = addr_port.split(':')
    expects(
        port.isdigit(),
        callback=ProxyInvalidError('port is not a number')
    )
    username, password = username_password.split(':')
    return Proxy(
        proxy_type=None,
        addr=addr,
        port=int(port),
        username=username,
        password=password
    )


def convert_at_symbol_proxy_with_protocol(proxy_string: str) -> Proxy:
    """protocol://user:pass@ip:port"""
    protocol, proxy_string = proxy_string.split('://')
    expects(
        protocol in ['socks5', 'socks5h', 'http', 'https'],
        ProxyInvalidError('protocol is invalid')
    )
    if protocol == 'https':
        protocol = 'http'
    elif protocol == 'socks5h':
        protocol = 'socks5'
    proxy = convert_at_symbol_proxy(proxy_string)
    proxy.proxy_type = protocol
    return proxy


def convert_regular_proxy(proxy_string: str) -> Proxy:
    """
    ip:port
    ip:port:user:pass
    """
    split_by_colon = proxy_string.split(':')
    expects(
        len(split_by_colon) in [2, 4],
        ProxyInvalidError('len(split_by_colon) != 2|4')
    )
    if len(split_by_colon) == 2:
        addr, port = split_by_colon
        username, password = None, None
    elif len(split_by_colon) == 4:
        addr, port, username, password = split_by_colon
    else:
        raise ProxyInvalidError('else statement at proxy_formats, line 61')

    return Proxy(
        proxy_type=None,
        addr=addr,
        port=int(port),
        username=username,
        password=password
    )


def convert_regular_proxy_with_protocol(proxy_string: str) -> Proxy:
    """
    protocol://ip:port
    protocol://ip:port:user:pass
    """
    protocol, proxy_string = proxy_string.split('://')
    expects(
        protocol in ['socks5', 'socks5h', 'http', 'https'],
        ProxyInvalidError('protocol is invalid')
    )
    if protocol == 'https':
        protocol = 'http'
    elif protocol == 'socks5h':
        protocol = 'socks5'
    proxy = convert_regular_proxy(proxy_string)
    proxy.proxy_type = protocol
    return proxy
