from __future__ import annotations
from typing import Dict
from enum import Enum


class TileType(Enum):
    Wall = 0
    Floor = 1

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

evergreen_1 = {
    'uid': 'evergreen_1',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['evergreen_1']
    }

evergreen_2 = {
    'uid': 'evergreen_2',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['evergreen_2'],
    }

evergreen_3 = {
    'uid': 'evergreen_3',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['evergreen_3'],
    }

boulder_1 = {
    'uid': 'boulder_1',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['boulder_1'],
    }

boulder_2 = {
    'uid': 'boulder_2',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['boulder_2'],
    }

boulder_3 = {
    'uid': 'boulder_3',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['boulder_3'],
    }

boulder_4 = {
    'uid': 'boulder_4',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['boulder_4'],
    }

rock_1 = {
    'uid': 'rock_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['rock_1'],
    }

rock_2 = {
    'uid': 'rock_2',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['rock_2'],
    }

grass_1 = {
    'uid': 'grass_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['grass_1'],
    }

grass_2 = {
    'uid': 'grass_2',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['grass_2'],
    }

brick_floor_TL = {
    'uid': 'brick_TL',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['brick_TL'],
    }

brick_floor_TR = {
    'uid': 'brick_TR',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['brick_TR'],
    }

brick_floor_L = {
    'uid': 'brick_L',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['brick_L'],
    }

brick_floor_T = {
    'uid': 'brick_T',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['brick_T'],
    }

brick_floor_R = {
    'uid': 'brick_R',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['brick_R'],
    }

brick_floor_M_1 = {
    'uid': 'brick_M_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['brick_M_1'],
    }

brick_left = {
    'uid': 'brick_wall_L',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['brick_wall_L'],
    }

brick_right = {
    'uid': 'brick_wall_R',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['brick_wall_R'],
    }

brick_bot_left = {
    'uid': 'brick_wall_BL',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['brick_wall_BL'],
    }

brick_bot_right = {
    'uid': 'brick_wall_BR',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['brick_wall_BR'],
    }

brick_wall = {
    'uid': 'brick_wall',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['brick_wall'],
    }

bare_floor = {
    'uid': 'blank',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank'],
    }

blank_floor = {
    'uid': 'bare_floor',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank'],
    }

blank_stone_floor = {
    'uid': 'blank_stone',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['blank_stone'],
    }

dirt_path = {
    'uid': 'dirt_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['dirt_1'],
    }

door_open = {
    'uid': 'door_open',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['door_open'],
    }

door_closed = {
    'uid': 'door_closed',
    'move_cost': TileType.Wall,
    'transparent': TileType.Wall,
    'char': all_tiles['door_closed'],
    }

stairs_down = {
    'uid': 'stairs_1',
    'move_cost': TileType.Floor,
    'transparent': TileType.Floor,
    'char': all_tiles['stairs_1'],
    }

tile_templates = {
    evergreen_1['uid']: evergreen_1,
    evergreen_2['uid']: evergreen_2,
    evergreen_3['uid']: evergreen_3,
    boulder_1['uid']: boulder_1,
    boulder_2['uid']: boulder_2,
    boulder_3['uid']: boulder_3,
    boulder_4['uid']: boulder_4,
    grass_1['uid']: grass_1,
    grass_2['uid']: grass_2,
    rock_1['uid']: rock_1,
    rock_2['uid']: rock_2,
    bare_floor['uid']: bare_floor,
    blank_floor['uid']: blank_floor,
    blank_stone_floor['uid']: blank_stone_floor,
    brick_floor_TL['uid']: brick_floor_TL,
    brick_floor_TR['uid']: brick_floor_TR,
    brick_floor_L['uid']: brick_floor_L,
    brick_floor_R['uid']: brick_floor_R,
    brick_floor_T['uid']: brick_floor_T,
    brick_floor_M_1['uid']: brick_floor_M_1,
    brick_left['uid']: brick_left,
    brick_right['uid']: brick_right,
    brick_bot_left['uid']: brick_bot_left,
    brick_bot_right['uid']: brick_bot_right,
    brick_wall['uid']: brick_wall,
    dirt_path['uid']: dirt_path,
    door_open['uid']: door_open,
    door_closed['uid']: door_closed,
    stairs_down['uid']: stairs_down,
    }

terrain_templates = {
    evergreen_1['uid']: evergreen_1,
    evergreen_2['uid']: evergreen_2,
    evergreen_3['uid']: evergreen_3,
    boulder_1['uid']: boulder_1,
    boulder_2['uid']: boulder_2,
    boulder_3['uid']: boulder_3,
    boulder_4['uid']: boulder_4,
    grass_1['uid']: grass_1,
    grass_2['uid']: grass_2,
    rock_1['uid']: rock_1,
    rock_2['uid']: rock_2,
    }

wall_templates = {
    brick_left['uid']: brick_left,
    brick_right['uid']: brick_right,
    brick_bot_left['uid']: brick_bot_left,
    brick_bot_right['uid']: brick_bot_right,
    brick_wall['uid']: brick_wall,
    }

floor_templates = {
    bare_floor['uid']: bare_floor,
    blank_floor['uid']: blank_floor,
    blank_stone_floor['uid']: blank_stone_floor,
    brick_floor_TL['uid']: brick_floor_TL,
    brick_floor_TR['uid']: brick_floor_TR,
    brick_floor_L['uid']: brick_floor_L,
    brick_floor_R['uid']: brick_floor_R,
    brick_floor_T['uid']: brick_floor_T,
    brick_floor_M_1['uid']: brick_floor_M_1,
    }

path_tempaltes = {
    dirt_path['uid']: dirt_path,
    }

portal_templates = {
    door_open['uid']: door_open,
    door_closed['uid']: door_closed,
    stairs_down['uid']: stairs_down,
    }

meta_templates = {
    blank_floor['uid']: blank_floor,
    blank_stone_floor['uid']: blank_stone_floor,
    }
