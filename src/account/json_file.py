# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Union

from opentele.api import APIData
from contextlib import contextmanager
from .account_info import AccountInfo

LANG_CODE_VARIATIONS = [
    'lang_code',
    'lang_pack'
]
SYSTEM_LANG_CODE_VARIATIONS = [
    'system_lang_code',
    'system_lang_pack'
]
TWOFA_VARIATIONS = [
    'twoFA',
    'two_fa',
    '2fa'
]
SYSTEM_VERSION_VARIATIONS = [
    'sdk',
    'system_version'
]
USER_ID_VARIATIONS = [
    'id',
    'user_id'
]


class JsonFile:
    """Represents a .json file for an account.
    Allows to extract APIData from it."""

    def __init__(self, json_file: Path):
        self.json_file = json_file
        self._file_data: dict[str, Union[str, int, bool]] = json.loads(self.json_file.read_text('utf-8'))
        # File absence must be handled by a higher level class like AccountLoader

    def __repr__(self):
        return f'JsonFile({self.json_file})'

    def get_key_safe(self, key: str):
        """Gets the JSON file key.
        Will return None if the key does not exist."""
        return self._file_data.get(key, None)

    def get_key_with_multiple_variations(self, variations: list[str]):
        """Fuck motherfuckers which decided that making different
        names of a single key in a json file is a good idea"""
        for variation in variations:
            value = self.get_key_safe(variation)
            if not value:
                continue
            else:
                return value
        return None

    @contextmanager
    def edit_json_file(self):
        """A context manager that will provide a dict with json data
        that can be edited. The changes will write to the file at exit"""
        self._file_data: dict[str, Union[str, int, bool]] = json.loads(self.json_file.read_text('utf-8'))
        try:
            yield self._file_data
        finally:
            self.json_file.write_text(json.dumps(self._file_data, ensure_ascii=False, indent=4))

    def extract_api_data(self) -> APIData:
        _api_id = self.get_key_safe('app_id')
        if isinstance(_api_id, str) and _api_id.isdigit():
            _api_id = int(_api_id)
        return APIData(
            api_id=_api_id,
            api_hash=self.get_key_safe('app_hash'),
            device_model=self.get_key_safe('device'),
            system_version=self.get_key_with_multiple_variations(SYSTEM_VERSION_VARIATIONS),
            app_version=self.get_key_safe('app_version'),
            lang_code=self.get_key_with_multiple_variations(LANG_CODE_VARIATIONS),
            lang_pack=self.get_key_with_multiple_variations(LANG_CODE_VARIATIONS),
            system_lang_code=self.get_key_with_multiple_variations(SYSTEM_LANG_CODE_VARIATIONS)
        )

    def get_account_info(self, api_data: APIData) -> AccountInfo:
        return AccountInfo(
            api_data=api_data,
            session_file=self.json_file.with_suffix('.session'),
            phone=self.get_key_safe('phone'),
            user_id=self.get_key_with_multiple_variations(USER_ID_VARIATIONS),
            register_time=self.get_key_safe('register_time'),
            first_name=self.get_key_safe('first_name'),
            last_name=self.get_key_safe('last_name'),
            username=self.get_key_safe('username'),
            twofa=self.get_key_with_multiple_variations(TWOFA_VARIATIONS)
        )
