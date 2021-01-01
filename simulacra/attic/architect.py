from __future__ import annotations
from typing import Callable, Generic, Generator, List, TypeVar, Tuple, TYPE_CHECKING

import numpy as np

from engine.util import classproperty
from engine.geometry.rect import Rect
from engine.rendering.tile import tile_dt, tile_graphic

if TYPE_CHECKING:
    from engine.areas.area import Area
    from engine.rendering.tile import Tile

T = TypeVar("T")
Vec = Tuple[int, int]


class Region:

    def __init__(self, name: str) -> None:
        self.name = name

    @classproperty
    def everywhere(self) -> Region:
        return Region("everywhere")

    @classproperty
    def north(self) -> Region:
        return Region("north")

    @classproperty
    def northeast(self) -> Region:
        return Region("northeast")

    @classproperty
    def east(self) -> Region:
        return Region("east")

    @classproperty
    def southeast(self) -> Region:
        return Region("southeast")

    @classproperty
    def south(self) -> Region:
        return Region("south")

    @classproperty
    def southwest(self) -> Region:
        return Region("southwest")

    @classproperty
    def west(self) -> Region:
        return Region("west")

    @classproperty
    def northwest(self) -> Region:
        return Region("northwest")

    @classproperty
    def directions(self) -> List[Region]:
        return [self.north,
                self.northeast,
                self.east,
                self.southeast,
                self.south,
                self.southwest,
                self.west,
                self.northwest,
                ]


class Array2D(Generic[T]):
    """Helper class that abstracts over a two-dimensional array. Useful for
    applying generators to area tiles."""

    def __init__(self, shape: Vec) -> None:
        self.width = shape[0]
        self.height = shape[1]
        self.tiles = np.full(shape, fill_value=0, order="F", dtype=tile_dt)

    def generated(self, shape: Vec, generator) -> None:
        self.width = shape[0]
        self.height = shape[1]
        self.tiles = np.full(shape, fill_value=0, order="F", dtype=tile_dt)

    def generate(self, generator) -> None:
        """Evaluates [generator] at each position in the array and sets the
        element at that position to the result.
        """
        for row in self.array[:]:
            for pos in row:
                generator(pos)

    def get_at_pos(self, pos: Vec) -> T:
        """Get the element in the array at [pos]."""
        return self.array[pos.xy]

    def set_at_pos(self, pos: Vec, value: T) -> None:
        """Set the element in the array at [pos] to [value]."""
        self.array[pos.xy] = value

    def fill(self, value: T) -> None:
        """Set every element in the array to [value]."""
        self.array = np.full((self.width, self.height), fill_value=value, order="F")

    def __getitem__(self, pos: Vec) -> Tile:
        return self.tiles[pos]


class Architect:
    """The main class that orchtestrates painting and populating the area."""

    def __init__(self, area: Area, depth: int) -> None:
        self.area = area
        self.depth = depth
        self._owners: Array2D[Architecture] = Array2D(shape=(area.width, area.height))
        self._carved_tiles: int = 0
        self._owners = {}

    def build_area(self, set_player_start: Callable[[Vec], None]) -> Area:
        pass

    @classmethod
    def owner_at(cls, pos: Vec) -> Architecture:
        pass

    def _carve(self, architecture: Architecture, x: int, y: int, tile: Tile) -> None:
        pass

    @property
    def _can_carve(self) -> bool:
        pass

    def _fill_passages(self):
        pass

    def _add_shortcuts(self):
        pass

    def _try_shortcut(self):
        pass

    def _is_shortcut(self):
        pass

    def _make_passage(self):
        pass

    def _claim_passages(self):
        pass

    def _claim_neighbors(self, pos: Vec, owner: Architecture) -> None:
        pass

    def _is_formed(self) -> bool:
        pass

    def _is_open_at(self) -> bool:
        pass

    def _is_solid_at(self) -> bool:
        pass


class Architecture:
    """Each architecture is a separate algorithm and some tuning prameters
    for it that generates part of the area."""

    def __init__(self) -> None:
        self._architect: Architect = None
        self._style: ArchitecturalStyle = None
        self._region = None


class ArchitecturalStyle:

    def __init__(self) -> None:
        self._styles = None  # should be a ResourceSet


class Decorator:

    def __init__(self) -> None:
        pass


class DensityMap:

    def __init__(self) -> None:
        pass


class Painter:
    """The procedural interface exposed by `Decorator` to let a `PaintStyle`
    modify the area."""

    def __init__(
            self,
            decorator: Decorator,
            architect: Architect,
            architecture: Architecture
        ) -> None:
        self._decorator = decorator
        self._architect = architect
        self._architecture = architecture
        self._painted: int = 0

    @property
    def bounds(self) -> Rect:
        return self._architect.area.shape