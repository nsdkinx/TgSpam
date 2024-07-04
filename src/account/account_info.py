# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from opentele.api import APIData
from datetime import datetime


@dataclass
class AccountInfo:
    """Main model representing the account information. Main source of it
    is the json file"""
    api_data: APIData
    session_file: Path
    phone: str
    user_id: int  # XXX: has multiple variations
    register_time: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    twofa: Optional[str] = None  # XXX: has multiple variations

    @property
    def register_datetime(self):
        """Returns the account registering time in datetime."""
        return datetime.fromtimestamp(self.register_time)

    @property
    def name(self):
        """Account first and last name combined."""
        if not self.last_name:
            return self.first_name
        return f'{self.first_name} {self.last_name}'

    @property
    def session_name(self):
        return self.session_file.name.removesuffix('.session')
