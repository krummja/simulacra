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

    wall = {

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
        'unknown1' : ( 0xE000, 0, 0 ),
        'unknown2' : ( 0xE000, 9, 0 ),
        'unknown3' : ( 0xE000, 9, 1 ),
        'unknown4' : ( 0xE000, 9, 2 ),
        'unknown5' : ( 0xE000, 9, 3 ),
        'unknown6' : ( 0xE000, 9, 4 ),
        'unknown7' : ( 0xE000, 9, 5 ),
        'unknown8' : ( 0xE000, 9, 6 ),
        'unknown9' : ( 0xE000, 9, 7 ),
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
