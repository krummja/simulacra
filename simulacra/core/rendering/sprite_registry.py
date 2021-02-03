from __future__ import annotations


class SpriteRegistry:

    ground = {
        'tile_1': (0xE000, 0, 0),
        'tile_2': (0xE000, 0, 1),
        }

    # tree = {
    #     'tree_1': (0xE000, 0, 0),
    #     'tree_2': (0xE000, 0, 1),
    #     'tree_3': (0xE000, 0, 2),
    #     }

    def get_codepoint(self, registry: str, uid: str):
        registry = getattr(self, registry)
        struct = registry[uid]
        return struct[0] + (16 * struct[1]) + struct[2]
