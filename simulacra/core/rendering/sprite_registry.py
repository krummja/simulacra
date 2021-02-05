class SpriteRegistry:

    SATURATED = 0x0
    DESATURATED = 0xC8

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

    other = {
        'unknown' : ( 0xE000, 0, 0 )
        }

    def get_codepoint(self, registry: str, uid: str, saturated: bool = True):
        registry = getattr(self, registry)
        struct = registry[uid]
        return struct[0] + (16 * struct[1]) + struct[2] + (0x0 if saturated else 0x200)
