from __future__ import annotations
from typing import Tuple, Dict
from enum import Enum
from hues import COLOR, Colors


color_list = [
    (25, 40, 40),
    (60, 60, 60),
    (100, 100, 60),
    (50, 140, 100),
    (135, 100, 70),
    (135, 100, 70),
    (100, 60, 40),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (100, 100, 100),
    (150, 150, 150),
    (0, 0, 0),
    (100, 150, 30),
    (0, 0, 0),
    (0, 0, 0)
    ]


wall_tiles: Dict[str, int] = {
    'boulder_1': 57344,
    'boulder_2': 57345,
    'boulder_3': 57346,
    'boulder_4': 57347,
    'evergreen_1': 57360,
    'evergreen_2': 57361,
    'evergreen_3': 57362,
    'bushes_1': 57363,
    'brick_1': 57376,
    'brick_2': 57377,
    'brick_3': 57378,
    'brick_4': 57379,
    'brick_5': 57380,
    'brick_6': 57381,
    'brick_wall_L': 57376,
    'brick_wall': 57377,
    'brick_wall_R': 57378,
    'brick_wall_BL': 57379,
    'brick_wall_BR': 57380,
    'slab_1': 57392,
    'slab_2': 57393,
    'window_1': 57408,
    }

door_tiles: Dict[str, int] = {
    'door_open': 57440,
    'door_closed': 57441,
    'stairs_1': 57442,
    }

ground_tiles: Dict[str, int] = {
    'blank': 0,
    'dirt_1': 57472,
    'dirt_2': 57473,
    'rock_1': 57474,
    'rock_2': 57475,
    'grass_1': 57488,
    'grass_2': 57489,
    }

floor_tiles: Dict[str, int] = {
    'brick_TL': 57504,
    'brick_T': 57505,
    'brick_TR': 57506,
    'blank_stone': 57507,
    'brick_L': 57520,
    'brick_M_1': 57521,
    'brick_R': 57522,
    }

all_tiles: Dict[str, int] = {
    'boulder_1': 57344,
    'boulder_2': 57345,
    'boulder_3': 57346,
    'boulder_4': 57347,
    'evergreen_1': 57360,
    'evergreen_2': 57361,
    'evergreen_3': 57362,
    'bushes_1': 57363,
    'brick_1': 57376,
    'brick_2': 57377,
    'brick_3': 57378,
    'brick_4': 57379,
    'brick_5': 57380,
    'brick_6': 57381,
    'brick_wall_L': 57376,
    'brick_wall': 57377,
    'brick_wall_R': 57378,
    'brick_wall_BL': 57379,
    'brick_wall_BR': 57380,
    'slab_1': 57392,
    'slab_2': 57393,
    'window_1': 57408,
    'door_open': 57440,
    'door_closed': 57441,
    'stairs_1': 57442,
    'blank': 0,
    'dirt_1': 57472,
    'dirt_2': 57473,
    'rock_1': 57474,
    'rock_2': 57475,
    'grass_1': 57488,
    'grass_2': 57489,
    'brick_TL': 57504,
    'brick_T': 57505,
    'brick_TR': 57506,
    'blank_stone': 57507,
    'brick_L': 57520,
    'brick_M_1': 57521,
    'brick_R': 57522,
    }


class TileType(Enum):
    Wall = 0
    Floor = 1

FOREST_FLOOR = (25, 40, 40)
INTERIOR_FLOOR = (60, 60, 60)

test_floor1 = {
    'uid': 'test1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['blank'],
    'color': (255, 0, 0),
    'bg': (100, 0, 0)
    }

test_floor2 = {
    'uid': 'test2',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['blank'],
    'color': (255, 0, 0),
    'bg': (255, 0, 0)
    }

test_floor3 = {
    'uid': 'test3',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['blank'],
    'color': (0, 0, 0),
    'bg': (50, 50, 200)
    }

test_floor4 = {
    'uid': 'test4',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['blank'],
    'color': (0, 0, 0),
    'bg': (100, 100, 255)
    }

bare_floor = {
    'uid': 'blank',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['blank'],
    'color': (255, 255, 255),
    'bg': FOREST_FLOOR
    }

blank_floor = {
    'uid': 'bare_floor',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['blank'],
    'color': (255, 255, 255),
    'bg': FOREST_FLOOR
    }

blank_stone_floor = {
    'uid': 'blank_stone',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': floor_tiles['blank_stone'],
    'color': (255, 255, 255),
    'bg': INTERIOR_FLOOR
    }

dirt_path = {
    'uid': 'dirt_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['dirt_1'],
    'color': (180, 100, 55),
    'bg': FOREST_FLOOR
    }

evergreen_1 = {
    'uid': 'evergreen_1',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['evergreen_1'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

evergreen_2 = {
    'uid': 'evergreen_2',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['evergreen_2'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

evergreen_3 = {
    'uid': 'evergreen_3',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['evergreen_3'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

boulder_1 = {
    'uid': 'boulder_1',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['boulder_1'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

boulder_2 = {
    'uid': 'boulder_2',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['boulder_2'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

boulder_3 = {
    'uid': 'boulder_3',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['boulder_3'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

boulder_4 = {
    'uid': 'boulder_4',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['boulder_4'],
    'color': (135, 100, 70),
    'bg': FOREST_FLOOR
    }

grass_1 = {
    'uid': 'grass_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['grass_1'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

grass_2 = {
    'uid': 'grass_2',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['grass_2'],
    'color': (45, 140, 100),
    'bg': FOREST_FLOOR
    }

brick_left = {
    'uid': 'brick_wall_L',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall_L'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

brick_right = {
    'uid': 'brick_wall_R',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall_R'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

brick_bot_left = {
    'uid': 'brick_wall_BL',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall_BL'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

brick_bot_right = {
    'uid': 'brick_wall_BR',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall_BR'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

brick_wall = {
    'uid': 'brick_wall',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': wall_tiles['brick_wall'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

rock_1 = {
    'uid': 'rock_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['rock_1'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

rock_2 = {
    'uid': 'rock_2',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': ground_tiles['rock_2'],
    'color': (100, 100, 100),
    'bg': FOREST_FLOOR
    }

door_open = {
    'uid': 'door_open',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': door_tiles['door_open'],
    'color': (100, 60, 40),
    'bg': FOREST_FLOOR
    }

door_closed = {
    'uid': 'door_closed',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': door_tiles['door_closed'],
    'color': (100, 60, 40),
    'bg': FOREST_FLOOR
    }

stairs_down = {
    'uid': 'stairs_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': door_tiles['stairs_1'],
    'color': (150, 150, 150),
    'bg': INTERIOR_FLOOR
    }

brick_floor_TL = {
    'uid': 'brick_TL',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': floor_tiles['brick_TL'],
    'color': (150, 150, 150),
    'bg': INTERIOR_FLOOR
    }

brick_floor_TR = {
    'uid': 'brick_TR',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': floor_tiles['brick_TR'],
    'color': (150, 150, 150),
    'bg': INTERIOR_FLOOR
    }

brick_floor_L = {
    'uid': 'brick_L',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': floor_tiles['brick_L'],
    'color': (150, 150, 150),
    'bg': INTERIOR_FLOOR
    }

brick_floor_T = {
    'uid': 'brick_T',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': floor_tiles['brick_T'],
    'color': (150, 150, 150),
    'bg': INTERIOR_FLOOR
    }

brick_floor_R = {
    'uid': 'brick_R',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': floor_tiles['brick_R'],
    'color': (150, 150, 150),
    'bg': INTERIOR_FLOOR
    }

brick_floor_M_1 = {
    'uid': 'brick_M_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': floor_tiles['brick_M_1'],
    'color': (150, 150, 150),
    'bg': INTERIOR_FLOOR
    }


tile_templates = {
    bare_floor['uid']: bare_floor,
    blank_floor['uid']: blank_floor,
    dirt_path['uid']: dirt_path,
    evergreen_1['uid']: evergreen_1,
    evergreen_2['uid']: evergreen_2,
    evergreen_3['uid']: evergreen_3,
    boulder_1['uid']: boulder_1,
    boulder_2['uid']: boulder_2,
    boulder_3['uid']: boulder_3,
    boulder_4['uid']: boulder_4,
    grass_1['uid']: grass_1,
    grass_2['uid']: grass_2,
    brick_left['uid']: brick_left,
    brick_right['uid']: brick_right,
    brick_bot_left['uid']: brick_bot_left,
    brick_bot_right['uid']: brick_bot_right,
    brick_wall['uid']: brick_wall,
    rock_1['uid']: rock_1,
    rock_2['uid']: rock_2,
    door_open['uid']: door_open,
    door_closed['uid']: door_closed,
    stairs_down['uid']: stairs_down,
    blank_stone_floor['uid']: blank_stone_floor,
    brick_floor_TL['uid']: brick_floor_TL,
    brick_floor_TR['uid']: brick_floor_TR,
    brick_floor_L['uid']: brick_floor_L,
    brick_floor_R['uid']: brick_floor_R,
    brick_floor_T['uid']: brick_floor_T,
    brick_floor_M_1['uid']: brick_floor_M_1,
    test_floor1['uid']: test_floor1,
    test_floor2['uid']: test_floor2,
    test_floor3['uid']: test_floor3,
    test_floor4['uid']: test_floor4
    }
