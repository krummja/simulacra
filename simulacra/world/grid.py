from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np

from simulacra.core.options import *


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
    transparent: np.ndarray
    visible: np.ndarray
    explored: np.ndarray

    def initialize_visibility(self) -> None:
        self.transparent = np.zeros((STAGE_WIDTH, STAGE_HEIGHT), dtype=np.bool, order="F")
        self.visible = np.zeros((STAGE_WIDTH, STAGE_HEIGHT), dtype=np.bool, order="F")
        self.explored = np.zeros((STAGE_WIDTH, STAGE_HEIGHT), dtype=np.bool, order="F")

        for x in range(self.width):
            for y in range(self.height):
                self.transparent[x][y] = self.tiles[x][y].entity['Tile'].transparent


class TileGrid(ProceduralTiles2D, InitRealTiles, VisibilityMixin):

    def __init__(self, area, width, height, variant=None) -> None:
        super().__init__(width, height, variant)
        self.area = area
        self.entrances = []
        self.exits = []
        self.tiles = None

    def fill_tiles(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                if isinstance(tile, Tile) and tile.UNFORMED:
                    real_tile = self.area._manager.game.ecs.engine.create_entity()
                    self.area._manager.game.ecs.engine.prefabs.apply_to_entity(
                        real_tile, 'Grass Tile', {'Position': {'x': x, 'y': y}}
                        )
                    tile.entity = real_tile
        self.initialize_visibility()

    def place_entities(self, room, area_type, subtype, power):
        pass
