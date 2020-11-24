from __future__ import annotations


test_item = {
    'uid': 'test_item',
    'name': 'Test Item',
    'description': 'A simple whatchamacallit. Nothing special.',
    'display': {
        'char': ord("!"),
        'color': (255, 0, 0),
        'bg': (0, 0, 0)
        }
    }

item_templates = {
    test_item['uid']: test_item
    }
