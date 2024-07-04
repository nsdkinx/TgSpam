# -*- coding: utf-8 -*-

import subprocess
import os


def execute_wmic_command(command: str) -> str:
    if os.name == 'posix':
        return 'YutaPerduks mode'
    raw_result = subprocess.check_output(command.split()).strip()
    value_only = raw_result.split(b'=')[1].decode()
    if value_only in ['', ' ', '\n']:
        return 'empty'
    else:
        return value_only
