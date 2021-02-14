from __future__ import annotations
from typing import Dict, Optional
import numpy as np
import tcod

from simulacra.core.options import *


class Workspace:

    def __init__(self) -> None:
        self.buildable = np.ones(STAGE_SHAPE, dtype=np.bool, order="F")
        self.owners = np.zeros(STAGE_SHAPE, dtype=np.int32, order="F")
        self.tiles = np.zeros(STAGE_SHAPE, dtype=np.int32, order="F")
        self.owner_list = []

    def set_owners(self, x: int, y: int, width: int, height: int, owner: int) -> None:
        self.owners[x:x+width, y:y+height] = owner


class Architect:

    def __init__(self, uid: int = 0) -> None:
        self.uid = uid
        self.tile_types: Dict[int, int] = {}

    def build(self):
        pass


class AreaBuilder:

    def new(self):
        workspace = Workspace()
        bsp = tcod.bsp.BSP(x=0, y=0, width=STAGE_WIDTH, height=STAGE_HEIGHT)
        bsp.split_recursive(depth=5,
                            min_width=3,
                            min_height=3,
                            max_horizontal_ratio=2,
                            max_vertical_ratio=2)

        for node in bsp.pre_order():
            if node.children:
                pass
            else:
                x, y = node.x, node.y
                w, h = node.width, node.height
                uid = (x + y + w + h)
                architect = Architect(uid=uid)
                workspace.set_owners(x, y, w, h, architect.uid)
                workspace.owner_list.append(uid)

        return workspace


if __name__ == '__main__':
    area_builder = AreaBuilder()
    workspace = area_builder.new()
    workspace.owner_list.sort()
    print(workspace.owner_list)
