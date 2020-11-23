from __future__ import annotations
from behaviors import base_ai


test_char = {
    'uid': 'test_character',
    'name': 'Test Character',
    'display': {
        'char': ord("T"),
        'color': (0, 255, 0),
        'bg': (0, 0, 0)
        },
    'control': base_ai.BasicNPC
    }


character_templates = {
    test_char['uid']: test_char
    }
