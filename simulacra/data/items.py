from __future__ import annotations


test_item = {
    'uid': 'test_item',
    'name': 'test item',
    'description': 'A simple whatchamacallit. Nothing special.',
    'display': {
        'char': ord("!"),
        'color': (255, 0, 0),
        'bg': (0, 0, 0)
        },
    'slot': None,
    'components': [('Physics', {'size': 'large'})]
    }

test_helmet = {
    'uid': 'test_helmet',
    'name': 'test helmet',
    'description': '',
    'display': {
        'char': 209,
        'color': (0, 255, 255),
        'bg': (0, 0, 0)
        },
    'slot': 'head',
    'components': [('Physics', {'size': 'large'})]
    }

test_breastplate = {
    'uid': 'test_breastplate',
    'name': 'test breastplate',
    'description': '',
    'display': {
        'char': ord("H"),
        'color': (0, 255, 255),
        'bg': (0, 0, 0)
        },
    'slot': 'torso',
    'components': [('Physics', {'size': 'large'})]
    }


item_templates = {
    test_item['uid']: test_item,
    test_helmet['uid']: test_helmet,
    test_breastplate['uid']: test_breastplate
    }
