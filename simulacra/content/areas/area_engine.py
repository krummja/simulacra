from __future__ import annotations
from typing import Generator, List, Tuple, Optional

from enum import Enum
import random
import numpy as np
import tcod

from engine.rendering.hues import COLOR
from content.architect.cellular_automata import Anneal, Amoeba, Conway, Life34, Bugs
from content.factories.tile_factory import TileFactory
from content.tiles.tile_defs import all_tiles, color_list
from engine.areas.area import Area
from engine.geometry.direction import Direction
from engine.geometry.circ import Circ
from engine.geometry.size import Size
from engine.geometry.point import Point
from engine.geometry.rect import Rect

from content.areas.structures.corridor import Corridor

from engine import apparata
from content.areas.generators.generators import Algorithm
from content.areas.generators.bsp import BinarySpacePartition
from content.areas.generators.room_builder import RoomBuilder


class Climate:

    def __init__(self) -> None:
        """Array representing a Whittaker diagram.

        Array is indexed [elevation, moisture] with elevation
        moving from highest to lowest, and mosture from wettest
        to driest.
        """
        self._data = np.zeros((4, 6), dtype=np.int)
        self._data[0, 0:3] = "SNOW"
        self._data[0, 3:4] = "TUNDRA"
        self._data[0, 4:5] = "BARE"
        self._data[0, 5:6] = "SCORCHED"
        self._data[1, 0:2] = "TAIGA"
        self._data[1, 2:4] = "SHRUBLAND"
        self._data[1, 4:6] = "TEMPERATE DESERT"
        self._data[2, 0:1] = "TEMPERATE RAINFOREST"
        self._data[2, 1:3] = "TEMPERATE FOREST"
        self._data[2, 3:5] = "GRASSLAND"
        self._data[2, 5:6] = "TEMPERATE DESERT"
        self._data[3, 0:2] = "TROPICAL RAINFOREST"
        self._data[3, 2:4] = "TROPICAL FOREST"
        self._data[3, 4:5] = "GRASSLAND"
        self._data[3, 5:6] = "SUBTROPICAL DESERT"

    @property
    def data(self) -> np.ndarray:
        return self._data


class AreaEngine:

    def __init__(self, area: Area) -> None:
        self.area = area
        self.owned = np.zeros(area.shape, dtype=np.int)
        self.working = np.zeros(area.shape, dtype=np.int)

    def generate(self):
        pass


class AreaPainter:

    def __init__(self, engine: AreaEngine) -> None:
        self.engine = engine
        self.tile_factory = TileFactory()

    def paint(self, uid, color=None, bg=None):
        if color is None:
            color = (255, 255, 255)
        if bg is None:
            bg = (0, 0, 0)
        return self.tile_factory.build(uid, color, bg)

    def paint_owners(self):
        tiles = self.engine.area.area_model.tiles
        tiles[...] = self.paint('bare_floor', bg=COLOR['nero'])


class Architect:

    def __init__(self, area: Area) -> None:
        """
        The Architect manages the Engine and the Painter.

        While the Engine dumbly chugs along, the Architect executes the larger plan of
        the area and tells the Engine what it can and cannot do, given some context.

        The Painter wraps the Engine and handles the actual area data mapping to tiles.
        The Architect again plays a role in this, resolving cases where the Painter
        may not have all of the necessary configuration to execute operations on the
        engine's data structures.
        """
        self.engine = AreaEngine(area)
        self.painter = AreaPainter(self.engine)

    def generate(self):
        self.engine.generate()
        self.painter.paint_owners()
