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
    'components': [('physics', {'size': 'large'}),
                   ('inventory')]
    }

item_templates = {
    test_item['uid']: test_item
    }
