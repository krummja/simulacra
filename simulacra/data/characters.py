from __future__ import annotations
from behaviors import base_ai


test_char = {
    'uid': 'test_character',
    'name': 'john smith',
    'display': {
        'char': ord("T"),
        'color': (0, 255, 0),
        'bg': (0, 0, 0)
        },
    'control': base_ai.BasicNPC
    }


test_char_2 = {
    'uid': 'test_character_2',
    'name': 'jane doe',
    'display': {
        'char': ord("U"),
        'color': (255, 0, 255),
        'bg': (0, 0, 0)
        },
    'control': base_ai.BasicNPC
    }


character_templates = {
    test_char['uid']: test_char,
    test_char_2['uid']: test_char_2
    }
