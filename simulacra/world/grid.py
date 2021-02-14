from __future__ import annotations

from abc import ABC
from collections import deque
from typing import Tuple


import numpy as np
import tcod
from simulacra.core.options import *
from simulacra.utils.geometry import Rect
from .algorithms import random_assets, RandomBuilding
from .abstracts.abstract_tiles import AbstractFillTiles, AbstractInitTiles
from .tile import Tile


class InitRealTiles(AbstractInitTiles):
    """Used by real TileGrids in the game."""

    def initialize_tiles(self):
        tiles = [[Tile() for x in range(self.width)]
                 for y in range(self.height)]
        self.tiles = tiles


class ProceduralTiles2D(AbstractInitTiles, AbstractFillTiles, ABC):
    """Abstract for procedurally generating Tile arrays based on given parameters."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        super().__init__()


class TileGrid(ProceduralTiles2D, InitRealTiles):

    def __init__(self, area, width, height) -> None:
        super().__init__(width, height)
        self.area = area
        self.tiles = None
        self.visible = np.zeros(STAGE_SHAPE, dtype=np.bool, order="F")
        self.explored = np.zeros(STAGE_SHAPE, dtype=np.bool, order="F")

    def generate(self):
        bsp = tcod.bsp.BSP(x=0, y=0, width=STAGE_WIDTH, height=STAGE_HEIGHT)
        bsp.split_recursive(depth=5,
                            min_width=3,
                            min_height=3,
                            max_horizontal_ratio=2,
                            max_vertical_ratio=2)

        rooms = deque([])
        for node in bsp.pre_order():
            if node.children:
                pass
            else:
                x, y = node.x, node.y
                w, h = node.width, node.height
                rooms.append(Rect.from_edges(left=x, top=y, right=x+w, bottom=y+h))

    def delegate_to_generator(self, generator: str, workspaces: deque[Tuple[Tile, Rect]]):
        algorithm = self.generators[generator]
        algorithm(workspaces.popleft())
        return workspaces

    def fill_tiles(self):
        ecs = self.area._manager.game.ecs
        random_assets(
            ecs,
            self.tiles,
            [( 'Grass Tile 1'   , 10 ),
             ( 'Grass Tile 2'   , 50 ),
             ( 'Grass Tile 3'   , 50 ),
             ( 'Flowers Tile 1' , 10 ),
             ( 'Flowers Tile 2' , 10 ),
             ( 'Tree Tile 1'    , 2 )
             ])

        RandomBuilding(ecs, self.tiles).build_walls()

