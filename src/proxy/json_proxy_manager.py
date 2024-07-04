# -*- coding: utf-8 -*-

import json
import logging
from pathlib import Path
from typing import Optional
from .model import Proxy

logger = logging.getLogger(__name__)


class JsonProxyManager:
    """Can get a proxy from account's json file
    and write a new proxy into it"""

    @classmethod
    def get_proxy_from_json_file(cls, json_file: Path) -> Optional[Proxy]:
        json_data = json.loads(json_file.read_text('utf-8'))
        if 'proxy' not in json_data:
            logger.info(f'JSON file {json_file}: not getting proxy because it\'s not in json_data')
            return None

        proxy_data: list = json_data['proxy']
        if not proxy_data:
            logger.info(f'JSON file {json_file}: not getting proxy because it\'s empty')
            return None

        if len(proxy_data) != 5:
            logger.info(f'JSON file {json_file}: not getting proxy because its length is not 5 (data: {proxy_data})')
            return None

        protocol_index, addr, port, username, password = proxy_data
        if protocol_index in [0, 3]:
            logger.info(f'JSON file {json_file}: protocol index is {protocol_index} so it\'s HTTP')
            proxy_type = 'http'
        else:
            logger.info(f'JSON file {json_file}: protocol index is {protocol_index} so it\'s SOCKS5')
            proxy_type = 'socks5'

        return Proxy(proxy_type, addr, port, username, password)

    @classmethod
    def write_proxy_into_json_file(cls, json_file: Path, proxy: Proxy):
        json_data = json.loads(json_file.read_text('utf-8'))
        if proxy.proxy_type == 'http':
            protocol_index = 3
        else:
            protocol_index = 2
        proxy_data = [protocol_index, proxy.addr, proxy.port, proxy.username, proxy.password]
        json_data['proxy'] = proxy_data
        logger.info(f'Writing {proxy} into JSON file {json_file}')
        json_file.write_text(
            json.dumps(json_data, ensure_ascii=False, indent=4),
            encoding='utf-8'
        )
