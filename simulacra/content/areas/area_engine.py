from __future__ import annotations
from typing import TYPE_CHECKING

from __future__ import annotations
from typing import List, Tuple, Optional

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

    def _generate_map_constituents(self):
        """
        In this phase of generation, the engine will use various procedural
        methods to create a set of individual map areas (constituents of the
        final map).
        """

    def _generate_base_map(self):
        """
        In this phase, the engine takes the rough constituents from the prior
        phase and attempts to find an optimal arrangement of them based on
        a graph grammar which specified what types of constituents may (not)
        branch from which others.
        """

    def _clean_up_map(self):
        """
        After arranging the pieces of the map, there are a lot of loose bits
        that need to be tidied, e.g. paths that lead nowhere, unconnected
        rooms, and bad pathing.
        """

    def _decorate_map(self):
        """
        Finally, the map data is applied to the actual area map, and
        appropriate tiles are replaced for their abstract counterparts.
        """
