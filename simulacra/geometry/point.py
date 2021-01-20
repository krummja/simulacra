"""ENGINE.GEOMETRY.Point"""
from __future__ import annotations

from typing import List, Tuple, Type, Union

from simulacra.utils.classproperty import classproperty

from .direction import Direction
from .size import Size


class Point(tuple):
    """Representation of a point using integer values.

    A Point object is defined as a tuple encoding its x,y components.
    Points can be indexed in row-major order using the property `Point.ij`.
    """

    def __new__(cls: Type[Point], x: int, y: int) -> Point:
        return tuple.__new__(cls, (x, y))

    @classproperty
    def origin(self) -> Point:
        """Origin point of the coordinate plane."""
        return Point(0, 0)

    @property
    def x(self) -> int:
        """Point object's x axis component."""
        return self[0]

    @property
    def y(self) -> int:
        """Point object's y axis component."""
        return self[1]

    @property
    def xy(self) -> Tuple[int, int]:
        """Cartesian x,y coordinates of this Point."""
        return self[0], self[1]

    @property
    def ij(self) -> Tuple[int, int]:
        """Row-major ordered coordinates of this Point."""
        return self[1], self[0]

    @property
    def neighbors(self) -> List[Point]:
        """Return a list of all neighboring Points."""
        return [self + d for d in Direction]

    def __add__(self, other: Union[Point, Direction]) -> Point:
        """Add this point to the components of either another Point or a
        Direction.
        """
        if isinstance(other, Direction):
            other = other.value
        elif isinstance(other, (Point, Size)):
            pass
        else:
            return NotImplemented
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other: Union[Point, Direction]) -> Point:
        """Subtract this point from the components of either another Point or a
        Direction.
        """
        if isinstance(other, Direction):
            other: Tuple[int, int] = other.value
        elif isinstance(other, (Point, Size)):
            pass
        else:
            return NotImplemented
        return Point(self.x - other[0], self.y - other[1])
