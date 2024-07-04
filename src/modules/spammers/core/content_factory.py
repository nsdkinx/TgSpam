# -*- coding: utf-8 -*-

from pathlib import Path

from modules.spammers.randomizable_text import RandomizableText
from .content import Content
from core.filesystem.container import files
from core.filesystem.helpers import is_file_empty


class ContentFactory:
    """Finds the content in the pm spammer content directory
    and loads it"""

    @staticmethod
    def _do_texts_exist(folder: Path) -> bool:
        """Checks if any text exists in the folder"""
        txt_files = list(folder.glob('*.txt'))
        if not txt_files:
            return False
        return all(not is_file_empty(txt_file) for txt_file in txt_files)

    def _get_content_folders(self) -> list[Path]:
        """Returns folders that has texts"""
        nested_folders = [obj for obj in files.spammer_content_folder.glob('*') if obj.is_dir()]
        not_empty_content_folder: list[Path] = []
        if not nested_folders:
            return []
        for folder in nested_folders:
            if self._do_texts_exist(folder):
                not_empty_content_folder.append(folder)
        return not_empty_content_folder
    
    def get_all_content(self) -> list[Content]:
        content_list: list[Content] = []
        content_folders = self._get_content_folders()
        for content_folder in content_folders:
            txt_files = list(content_folder.glob('*.txt'))
            content_list.append(
                Content(
                    name=content_folder.name,
                    texts=[
                        RandomizableText(text_file.name, text_file.read_text('utf-8'))
                        for text_file in txt_files
                    ],
                    media=list(content_folder.glob('*.png')) + list(content_folder.glob('*.mp4')) + list(content_folder.glob('*.jpg'))
                )
            )
        return content_list


content_factory = ContentFactory()
