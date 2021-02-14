
from abc import ABC, abstractmethod


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
