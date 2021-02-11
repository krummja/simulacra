from dataclasses import dataclass
import numpy as np
from enum import IntFlag
from math import cos, sin, pi


class Wall(IntFlag):
    EAST = 2**0
    SOUTH = 2**1
    WEST = 2**2
    NORTH = 2**3


def fetch_wall(pos, walkable_space):
    x, y = pos
    height, width = walkable_space.shape
    if walkable_space[x, y]:
        return 0

    wall = 0
    for i in range(4):
        dx, dy = round(cos(i * pi / 2), round(sin(i * pi / 2)))
        if 0 <= y + dy < height and 0 <= x + dx < width:
            wall += (not walkable_space[x + dx, y + dy]) * 2**i
    return wall


class SpriteRegistry:

    SATURATED = 0x0
    DESATURATED = 0x200

    ground = {
        'green_1'     : ( 0xE000, 0,  0 ),
        'green_2'     : ( 0xE000, 0,  1 ),
        'parchment'   : ( 0xE000, 0,  2 ),
        'transparent' : ( 0xE000, 0,  3 ),
        }

    decoration = {
        'pebbles_1'   : ( 0xE000, 1,  0 ),
        'pebbles_2'   : ( 0xE000, 1,  1 ),
        'stones_1'    : ( 0xE000, 1,  2 ),
        'stones_2'    : ( 0xE000, 1,  3 ),
        'grass_1'     : ( 0xE000, 2,  0 ),
        'grass_2'     : ( 0xE000, 2,  1 ),
        'flowers_1'   : ( 0xE000, 2,  4 ),
        'flowers_2'   : ( 0xE000, 2,  5 ),
        }

    tree = {
        'tree_1' : ( 0xE000,  3,  0 ),
        'tree_2' : ( 0xE000,  3,  1 ),
        'tree_3' : ( 0xE000,  3,  2 ),
        }

    path = {
        'corner_top_left'             : ( 0xE000, 0, 4 ),
        'corner_top_right'            : ( 0xE000, 0, 5 ),
        'corner_bottom_left'          : ( 0xE000, 1, 4 ),
        'corner_bottom_right'         : ( 0xE000, 0, 5 ),

        'inverse_corner_top_left'     : ( 0xE000, 0, 6 ),
        'inverse_corner_top'          : ( 0xE000, 0, 7 ),
        'inverse_corner_top_right'    : ( 0xE000, 0, 8 ),
        'inverse_corner_left'         : ( 0xE000, 1, 6 ),
        'inverse_corner_right'        : ( 0xE000, 1, 8 ),
        'inverse_corner_bottom_left'  : ( 0xE000, 2, 6 ),
        'inverse_corner_bottom'       : ( 0xE000, 2, 7 ),
        'inverse_corner_bottom_right' : ( 0xE000, 2, 8 ),

        'turn_top_left'               : ( 0xE000, 0, 10 ),
        'turn_top_right'              : ( 0xE000, 0, 11 ),
        'turn_bottom_left'            : ( 0xE000, 0,  9 ),
        'turn_bottom_right'           : ( 0xE000, 1, 11 ),
        'fork_left'                   : ( 0xE000, 1,  9 ),
        'fork_top'                    : ( 0xE000, 1, 10 ),
        'fork_right'                  : ( 0xE000, 2,  9 ),
        'fork_bottom'                 : ( 0xE000, 2, 10 ),
        'four_way'                    : ( 0xE000, 2, 11 ),

        'single_tile'                 : ( 0xE000, 3,  9 ),
        'end_left'                    : ( 0xE000, 3, 10 ),
        'horizontal'                  : ( 0xE000, 3, 11 ),
        'end_right'                   : ( 0xE000, 3, 12 ),
        'end_top'                     : ( 0xE000, 0, 12 ),
        'vertical'                    : ( 0xE000, 1, 12 ),
        'end_bottom'                  : ( 0xE000, 2, 12 ),
        }

    structure = {
        'wall': {
            'inner_endcap_right' : ( 0xE000, 4, 0 ),
            'inner_endcap_left'  : ( 0xE000, 4, 1 ),
            'inner_horizontal'   : ( 0xE000, 4, 2 ),
            'inner_top_left'     : ( 0xE000, 4, 3 ),
            'inner_top_right'    : ( 0xE000, 4, 4 ),
            'inner_bottom_left'  : ( 0xE000, 4, 5 ),
            'inner_bottom_right' : ( 0xE000, 4, 6 ),
            'inner_left'         : ( 0xE000, 4, 7 ),
            'inner_right'        : ( 0xE000, 4, 8 ),
            'facing_outer'       : ( 0xE000, 5, 0 ),
            'facing_inner'       : ( 0xE000, 5, 1 ),
            'facing_left'        : ( 0xE000, 5, 2 ),
            'facing_right'       : ( 0xE000, 5, 3 ),
            },
        'door': {
            'inner_open'         : ( 0xE000, 4,  9 ),
            'facing_open'        : ( 0xE000, 5,  9 ),
            'inner_closed'       : ( 0xE000, 4, 10 ),
            'facing_closed'      : ( 0xE000, 5, 10 ),
            },
        'floor': {
            'top_left'       : ( 0xE000, 6, 0 ),
            'top'            : ( 0xE000, 6, 1 ),
            'top_right'      : ( 0xE000, 6, 2 ),
            'center_bare'    : ( 0xE000, 6, 3 ),
            'left'           : ( 0xE000, 7, 0 ),
            'center_bricks'  : ( 0xE000, 7, 1 ),
            'right'          : ( 0xE000, 7, 2 ),
            'bottom_left'    : ( 0xE000, 8, 0 ),
            'bottom'         : ( 0xE000, 8, 1 ),
            'bottom_right'   : ( 0xE000, 8, 2 ),
            }
        }

    dungeon = {
        'wall': {
            'brick_1' : ( 0xE000, 11, 1 ),
            'brick_2' : ( 0xE000, 11, 2 ),
            'brick_3' : ( 0xE000, 11, 3 ),
            'void'    : ( 0xE000, 11, 5 ),
            },
        'floor': {
            'stone_1' : ( 0xE000, 12, 1 ),
            'stone_2' : ( 0xE000, 12, 2 ),
            'stone_3' : ( 0xE000, 12, 3 ),
            'stone_4' : ( 0xE000, 13, 0 ),
            'stone_5' : ( 0xE000, 13, 1 ),
            'stone_6' : ( 0xE000, 13, 3 ),
            'stone_7' : ( 0xE000, 14, 1 ),
            'stone_8' : ( 0xE000, 14, 2 ),
            'stone_9' : ( 0xE000, 14, 3 ),
            'gap'     : ( 0xE000, 13, 2 ),
            },
        'border': {
            'northwest'       : ( 0xE000, 10, 0 ),
            'north'           : ( 0xE000, 10, 1 ),
            'northeast'       : ( 0xE000, 10, 4 ),
            'west'            : ( 0xE000, 11, 0 ),
            'east'            : ( 0xE000, 11, 4 ),
            'southwest'       : ( 0xE000, 15, 0 ),
            'south'           : ( 0xE000, 15, 1 ),
            'southeast'       : ( 0xE000, 15, 4 ),
            'northwest_inner' : ( 0xE000, 12, 0 ),
            'northeast_inner' : ( 0xE000, 12, 4 ),
            'southwest_inner' : ( 0xE000, 14, 0 ),
            'southeast_inner' : ( 0xE000, 14, 4 ),
            }
        }

    other = {
        'unknown1' : ( 0xEF00, 0, 15 ),
        'unknown2' : ( 0xEF00, 0,  8 ),
        'unknown3' : ( 0xEF00, 0,  9 ),
        'unknown4' : ( 0xEF00, 0, 10 ),
        'unknown5' : ( 0xEF00, 0, 11 ),
        'unknown6' : ( 0xEF00, 0, 12 ),
        'unknown7' : ( 0xEF00, 0, 13 ),
        'unknown8' : ( 0xEF00, 0, 14 ),
        'unknown9' : ( 0xEF00, 0, 15 ),
        }

    def get_codepoint(self, registry: str, uid: str, saturated: bool = True):
        registry = getattr(self, registry)
        tag_list = uid.split("/")
        if len(tag_list) > 1:
            subregistry = tag_list[0]
            uid = tag_list[1]
            struct = registry[subregistry][uid]
        else:
            struct = registry[uid]
        return struct[0] + (16 * struct[1]) + struct[2] + (
            self.SATURATED if saturated else self.DESATURATED
            )
