# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class License:
    license_key: str
    activated_modules: list[str]
    expiry_days: int
