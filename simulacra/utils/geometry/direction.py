"""ENGINE.GEOMETRY.Direction"""
from __future__ import annotations
from typing import Tuple

from enum import Enum

from simulacra.utils.classproperty import classproperty


class Direction(Enum):
    """Enum of normalized orthogonal and diagonal directions."""

    here: Tuple[int, int] = (0, 0)
    up: Tuple[int, int] = (0, -1)
    up_right: Tuple[int, int] = (1, -1)
    right: Tuple[int, int] = (1, 0)
    down_right: Tuple[int, int] = (1, 1)
    down: Tuple[int, int] = (0, 1)
    down_left: Tuple[int, int] = (-1, 1)
    left: Tuple[int, int] = (-1, 0)
    up_left: Tuple[int, int] = (-1, -1)

    @classproperty
    def orthogonals(self) -> frozenset:
        """Return frozen set of the four cardinal directions."""
        return frozenset((self.up, self.down, self.left, self.right))

    @classproperty
    def diagonals(self) -> frozenset:
        """Return frozen set of the four diagonal directions."""
        return frozenset((self.up_left, self.up_right, self.down_left, self.down_right))

    @property
    def opposite(self) -> Direction:
        """Return the opposite of a direction."""
        # pylint: disable=unsubscriptable-object
        return Direction((-self.value[0], -self.value[1]))

    def is_adjacent_to(self, other) -> bool:
        """Check if one position is adjacent to the this position."""
        # pylint: disable=unsubscriptable-object
        return ((self.value[0] == other.value[0] and
                abs(self.value[1] - other.value[1]) <= 1) or
                (self.value[1] == other.value[1] and
                abs(self.value[0] - other.value[0]) <= 1))
