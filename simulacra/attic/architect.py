from __future__ import annotations
from typing import Callable, Generic, Generator, List, TypeVar, Tuple, TYPE_CHECKING

import numpy as np

from engine.util import classproperty
from engine.geometry.rect import Rect
from engine.tiles.tile import tile_dt, tile_graphic

if TYPE_CHECKING:
    from engine.areas.area import Area
    from engine.tiles.tile import Tile

T = TypeVar("T")


class DensityMap:

    def __init__(self) -> None:
        pass


