# -*- coding: utf-8 -*-
import traceback
from pathlib import Path


class FileList(list):

    def __init__(self, seq=None, filename: Path = None):
        super().__init__()
        if not seq and filename:
            self.filename = filename
        elif seq and not filename:
            # Fucking asdict hack
            self.filename = None
            self.seq = seq
        self.load_items()

    def load_items(self):
        if not self.filename:
            return
        with self.filename.open('r+', encoding='utf-8') as file:
            self.extend([line.strip() for line in file.readlines()])

    def save_items(self):
        if not self.filename:
            return
        with self.filename.open('w+', encoding='utf-8') as file:
            file.write('\n'.join(self))

    def append(self, item):
        super().append(item)
        self.save_items()

    def remove(self, item):
        super().remove(item)
        self.save_items()

    def pop(self, index=-1):
        item = super().pop(index)
        self.save_items()
        return item

    def extend(self, iterable):
        super().extend(iterable)
        self.save_items()

    def clear(self):
        super().clear()
        self.save_items()

    def __len__(self):
        try:
            return super().__len__()
        except BaseException:
            traceback.print_exc()
            return 0
