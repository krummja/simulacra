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
    'name': 'Simple Helmet',
    'description': '',
    'display': {
        'char': 57616,
        'color': (0, 255, 255),
        'bg': (0, 0, 0)
        },
    'slot': 'head',
    'components': [('Physics', {'size': 'large'})]
    }

test_breastplate = {
    'uid': 'test_breastplate',
    'name': 'Simple Breastplate',
    'description': '',
    'display': {
        'char': ord("H"),
        'color': (0, 255, 255),
        'bg': (0, 0, 0)
        },
    'slot': 'torso',
    'components': [('Physics', {'size': 'large'})]
    }

test_chest = {
    'uid': 'test_chest',
    'name': 'Chest',
    'description': '',
    'display': {
        'char': 57648,
        'color': (200, 100, 100),
        'bg': (0, 0, 0),
        },
    'slot': None,
    'components': [('Physics', {'size': 'large'})]
    }

test_scroll = {
    'uid': 'test_scroll',
    'name': 'Scroll',
    'description': '',
    'display': {
        'char': 57632,
        'color': (255, 122, 78),
        'bg': (0, 0, 0),
        },
    'slot': None,
    'components': [('Physics', {'size': 'large'})]
    }

test_longsword = {
    'uid': 'test_longsword',
    'name': 'Longsword',
    'description': '',
    'display': {
        'char': 57600,
        'color': (255, 255, 255),
        'bg': (0, 0, 0)
        },
    'slot': 'right_hand',
    'components': [('Physics', {'size': 'large'})]
    }


item_templates = {
    test_item['uid']: test_item,
    test_helmet['uid']: test_helmet,
    test_breastplate['uid']: test_breastplate,
    test_chest['uid']: test_chest,
    test_scroll['uid']: test_scroll,
    test_longsword['uid']: test_longsword,
    }
