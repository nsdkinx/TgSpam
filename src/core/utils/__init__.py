# -*- coding: utf-8 -*-

from pathlib import Path
if Path('smm_debug_mode').exists():
    DEBUG_MODE = True
else:
    DEBUG_MODE = False
