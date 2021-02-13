from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Tuple

import random

import numpy as np
import tcod
from simulacra.core.options import *
from simulacra.utils.geometry import Rect
from .algorithms import random_grass, random_assets


class AbstractInitTiles(ABC):
    """Abstract for creating an array of Tile entities."""

    def __init__(self):
        self.tiles = self.initialize_tiles()

    @abstractmethod
    def initialize_tiles(self):
        pass


class AbstractFillTiles(ABC):
    """Abstract for filling an array of Tile entities."""

    @abstractmethod
    def fill_tiles(self):
        pass


class Tile:
    """Nonce class for a tile that has not been replaced by a concrete entity."""

    UNFORMED = True
    PASSABLE = True

    @property
    def passable(self) -> bool:
        return self.PASSABLE

    @passable.setter
    def passable(self, value: bool) -> None:
        self.PASSABLE = value

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        self.UNFORMED = False
        self._entity = value


class InitRealTiles(AbstractInitTiles):
    """Used by real TileGrids in the game."""

    def initialize_tiles(self):
        tiles = [[Tile() for x in range(self.width)]
                 for y in range(self.height)]
        self.tiles = tiles


class ProceduralTiles2D(AbstractInitTiles, AbstractFillTiles, ABC):
    """Abstract for procedurally generating Tile arrays based on given parameters."""

    def __init__(self, width: int, height: int, variant) -> None:
        self.width = width
        self.height = height
        self.variant = variant
        super().__init__()


class VisibilityMixin:

    visible = np.zeros((STAGE_WIDTH, STAGE_HEIGHT), dtype=np.bool, order="F")
    explored = np.zeros((STAGE_WIDTH, STAGE_HEIGHT), dtype=np.bool, order="F")


class RandomSelection:

    def __init__(self, workspace: Workspace) -> None:
        self.workspace = workspace
        self.random_selection('grass_1')

    def random_selection(self, tile):
        print(self.workspace)
        return self.workspace


@dataclass
class Workspace:
    tiles: deque[Tile]
    rect: Rect


class TileGrid(ProceduralTiles2D, InitRealTiles, VisibilityMixin):

    def __init__(self, area, width, height, variant=None) -> None:
        super().__init__(width, height, variant)
        self.area = area
        self.tiles = None
        self.generators = {
            'random': RandomSelection
            }

    def generate(self):
        tile_count = STAGE_WIDTH * STAGE_HEIGHT
        formed_tiles = 0

        #! We're going to start out by running a BSP to divide up the area.
        bsp = tcod.bsp.BSP(x=0, y=0, width=STAGE_WIDTH, height=STAGE_HEIGHT)
        bsp.split_recursive(
            depth=5,
            min_width=3,
            min_height=3,
            max_horizontal_ratio=2,
            max_vertical_ratio=2,
            )

        #! We'll store the terminal nodes as Rect objects in a List.
        rooms = deque([])
        for node in bsp.pre_order():
            if node.children:
                pass
            else:
                x, y = node.x, node.y
                w, h = node.width, node.height
                rooms.append(Rect.from_edges(left=x, top=y, right=x+w, bottom=y+h))

        #! Now we can start working with them! One way to do this might be to
        #! pass Rects to other generators, then get them back and map them to the grid.

        completed = deque([])
        while len(rooms) > 0:
            room = rooms.popleft()
            workspaces = deque([])
            for x in range(room.horizontal_span.start, room.horizontal_span.end):
                for y in range(room.vertical_span.start, room.vertical_span.end):
                    tiles = deque([])
                    tiles.append(self.tiles[x][y])
                    workspaces.append(Workspace(tiles, room))

            workspaces = self.delegate_to_generator('random', workspaces)

            completed.append(room)

        #! Grab any outlier unformed tiles to clean up.
        unformed = []
        for x in range(self.width):
            for y in range(self.height):
                if not self.tiles[x][y].UNFORMED:
                    continue
                tile = self.tiles[x][y]
                unformed.append(tile)

    def delegate_to_generator(self, generator: str, workspaces: deque[Tuple[Tile, Rect]]):
        #! Toss a List of workspaces to a generator for generation!
        algorithm = self.generators[generator]
        algorithm(workspaces.popleft())
        return workspaces

    def fill_tiles(self):
        """Fill the entire area with an actual entity which has a Tile component."""
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

    def place_entities(self, room, area_type, subtype, power):
        pass
