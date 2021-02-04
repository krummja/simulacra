class SpriteRegistry:

    ground = {
        'tile_1': (0xE000, 0, 0),
        'tile_2': (0xE000, 0, 1),
        'tile_3': (0xE000, 0, 2),
        'tile_4': (0xE000, 0, 3),
        'pebbles_1': (0xE000, 0, 4),
        'pebbles_2': (0xE000, 0, 4),
        }

    wall = {
        'wall_left_1': (0xE000, 3, 0),
        'wall_left_2': (0xE000, 4, 0),
        'wall_left_3': (0xE000, 5, 0),
        'wall_left_4': (0xE000, 6, 0),
        'wall_top_1': (0xE000, 3, 1),
        'wall_top_2': (0xE000, 3, 2),
        'wall_top_3': (0xE000, 3, 3),
        'wall_top_4': (0xE000, 3, 4),
        'wall_right_1': (0xE000, 3, 5),
        'wall_right_2': (0xE000, 4, 5),
        'wall_right_3': (0xE000, 5, 5),
        'wall_right_4': (0xE000, 6, 5),
        'wall_bottom_1': (0xE000, 7, 1),
        'wall_bottom_2': (0xE000, 7, 2),
        'wall_bottom_3': (0xE000, 7, 3),
        'wall_bottom_4': (0xE000, 7, 4),
        'wall_left_corner': (0xE000, 7, 0),
        'wall_right_corner': (0xE000, 7, 5),
        }

    def get_codepoint(self, registry: str, uid: str):
        registry = getattr(self, registry)
        struct = registry[uid]
        return struct[0] + (16 * struct[1]) + struct[2]
