from __future__ import annotations

from engine.rendering import COLOR


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
        'char': 57617,
        'color': COLOR['silver'],
        'bg': (0, 0, 0)
        },
    'slot': 'head',
    'components': [('Physics', {'size': 'large'})]
    }

test_cuirass = {
    'uid': 'test_cuirass',
    'name': 'Simple Cuirass',
    'description': '',
    'display': {
        'char': 57618,
        'color': COLOR['silver'],
        'bg': (0, 0, 0)
        },
    'slot': 'torso',
    'components': [('Physics', {'size': 'large'})]
    }

test_greaves = {
    'uid': 'test_greaves',
    'name': 'Simple Greaves',
    'description': '',
    'display': {
        'char': 57619,
        'color': COLOR['silver'],
        'bg': (0, 0, 0)
        },
    'slot': 'legs',
    'components': [('Physics', {'size': 'large'})]
    }

test_belt = {
    'uid': 'test_belt',
    'name': 'Simple Belt',
    'description': '',
    'display': {
        'char': 57620,
        'color': COLOR['brown'],
        'bg': (0, 0, 0)
        },
    'slot': 'waist',
    'components': [('Physics', {'size': 'large'})]
    }

test_boots = {
    'uid': 'test_boots',
    'name': 'Simple Boots',
    'description': '',
    'display': {
        'char': 57621,
        'color': COLOR['brown'],
        'bg': (0, 0, 0)
        },
    'slot': 'feet',
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
        'color': COLOR['silver'],
        'bg': (0, 0, 0)
        },
    'slot': 'right_hand',
    'components': [('Physics', {'size': 'large'})]
    }


item_templates = {
    test_item['uid']: test_item,
    test_helmet['uid']: test_helmet,
    test_cuirass['uid']: test_cuirass,
    test_greaves['uid']: test_greaves,
    test_belt['uid']: test_belt,
    test_boots['uid']: test_boots,
    test_chest['uid']: test_chest,
    test_scroll['uid']: test_scroll,
    test_longsword['uid']: test_longsword,
    }
