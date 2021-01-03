from __future__ import annotations
from typing import Dict, Optional, List, Union
from enum import Enum
from collections import defaultdict

import numpy as np

FOREST_FLOOR = (25, 40, 40)
INTERIOR_FLOOR = (60, 60, 60)

floor_tiles: Dict[str, int] = {
    'brick_nw': 57504,
    'brick_n': 57505,
    'brick_ne': 57506,
    'blank_stone': 57507,
    'brick_w': 57520,
    'brick_m1': 57521,
    'brick_e': 57522,
    }


# brick_floor_TL = {
#     'uid': 'brick_TL',
#     'move_cost': TileType.Floor,
#     'transparent': TileType.Floor,
#     'char': floor_tiles['brick_TL'],
#     'color': (150, 150, 150),
#     'bg': INTERIOR_FLOOR
#     }

# brick_floor_TR = {
#     'uid': 'brick_TR',
#     'move_cost': TileType.Floor,
#     'transparent': TileType.Floor,
#     'char': floor_tiles['brick_TR'],
#     'color': (150, 150, 150),
#     'bg': INTERIOR_FLOOR
#     }

# brick_floor_L = {
#     'uid': 'brick_L',
#     'move_cost': TileType.Floor,
#     'transparent': TileType.Floor,
#     'char': floor_tiles['brick_L'],
#     'color': (150, 150, 150),
#     'bg': INTERIOR_FLOOR
#     }

# brick_floor_T = {
#     'uid': 'brick_T',
#     'move_cost': TileType.Floor,
#     'transparent': TileType.Floor,
#     'char': floor_tiles['brick_T'],
#     'color': (150, 150, 150),
#     'bg': INTERIOR_FLOOR
#     }

# brick_floor_R = {
#     'uid': 'brick_R',
#     'move_cost': TileType.Floor,
#     'transparent': TileType.Floor,
#     'char': floor_tiles['brick_R'],
#     'color': (150, 150, 150),
#     'bg': INTERIOR_FLOOR
#     }

# brick_floor_M_1 = {
#     'uid': 'brick_M_1',
#     'move_cost': TileType.Floor,
#     'transparent': TileType.Floor,
#     'char': floor_tiles['brick_M_1'],
#     'color': (150, 150, 150),
#     'bg': INTERIOR_FLOOR
#     }

floor_templates = {
    # brick_floor_TL['uid']: brick_floor_TL,
    # brick_floor_TR['uid']: brick_floor_TR,
    # brick_floor_L['uid']: brick_floor_L,
    # brick_floor_R['uid']: brick_floor_R,
    # brick_floor_T['uid']: brick_floor_T,
    # brick_floor_M_1['uid']: brick_floor_M_1,
}
