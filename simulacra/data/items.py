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
    'components': [('Physics', {'size': 'large'}),
                   ('Inventory', {'slots': 3})]
    }

other_item = {
    'uid': 'other_item',
    'name': 'other item',
    'description': 'A simple whatchamacallit. Nothing special.',
    'display': {
        'char': ord("*"),
        'color': (0, 255, 255),
        'bg': (0, 0, 0)
        },
    'components': [('Physics', {'size': 'large'}),
                   ('Inventory', {'slots': 3})]
    }

item_templates = {
    test_item['uid']: test_item,
    other_item['uid']: other_item
    }
