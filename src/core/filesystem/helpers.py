# -*- coding: utf-8 -*-

from pathlib import Path


def is_file_empty(file: Path, create_if_not_exists: bool = False) -> bool:
    """Checks is the file provided is empty"""
    if not file.exists():
        if create_if_not_exists:
            file.touch()  # Was commented, may create errors or bugs
        return True

    data = file.read_text('utf-8')

    return not data.strip()
