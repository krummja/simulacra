from __future__ import annotations
from typing import TYPE_CHECKING

from config import *


base_template = {
    'uid': 'base_template',
    'title': 'BASE TEMPLATE',
    'x': 2,
    'y': 2,
    'width': 30,
    'height': 10,
    'framed': True,
}


test_element = {
    'uid': 'test_element',
    'name': 'test element',
    'position': { 'x': 2, 'y': 2 },
    'size': { 'width': 20, 'height': 10 },
    'style': {'framed': True},
    'content': "<empty>"
}


interface_templates = {
    base_template['uid']: base_template
}

# Non-Template Configs (Legacy UI)

bar_config = {
        'position': ('top', 'left')
    }

xp_config = {
    'position': ('top', 'left'),
    'offset_x': 8, 'margin': 0, 'width': 24,
    'text_fg': (255, 255, 255),
    }

character_panel = {
    'position': ('top', 'right'),
    'size': {
        'width': SIDE_PANEL_WIDTH,
        'height': (SIDE_PANEL_HEIGHT // 3)
        },
    'style': {'framed': True}
    }

player_info_panel = {
    'position': ('top', 'left'),
    'offset': {'x': 2, 'y': 2},
    'size': {'width': SIDE_PANEL_WIDTH-3, 'height': 4},
    }


nearby_panel = {
    'position': ('top', 'right'),
    'offset': {'y': (SIDE_PANEL_HEIGHT // 3)},
    'size': {'width': SIDE_PANEL_WIDTH, 'height': 8},
    'style': {'title': " nearby ", 'framed': True}
    }

inventory_panel = {
    'position': ('bottom', 'right'),
    'offset_x': -(SIDE_PANEL_WIDTH // 2),
    'width': SIDE_PANEL_WIDTH // 2,
    'height': (SIDE_PANEL_HEIGHT // 2) + 2,
    'title': "INVENTORY", 
    'framed': True
    }

equipment_panel = {
    'position': ('bottom', 'right'),
    'width': SIDE_PANEL_WIDTH // 2,
    'height': (SIDE_PANEL_HEIGHT // 2) + 2,
    'framed': True,
    'title': "EQUIPMENT"
    }

delete = {
    'position': ('center', 'center'),
    'size': {
        'width': 20,
        'height': 5,
    },
    'style': {'framed': True}
}