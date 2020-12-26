from __future__ import annotations
from typing import Tuple, Type

from enum import Enum
import numpy as np

from util import classproperty


class Direction(Enum):
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
    def orthogonal(self):
        return frozenset(
            (self.up, self.down, self.left, self.right)
            )

    @classproperty
    def diagonal(self):
        return frozenset(
            (self.up_left, self.up_right, self.down_left, self.down_right)
            )

    @property
    def opposite(self):
        return Direction((-self.value[0], -self.value[1]))

    def adjacent_to(self, other):
        return ((self.value[0] == other.value[0] and
                abs(self.value[1] - other.value[1]) <= 1) or
                (self.value[1] == other.value[1] and
                abs(self.value[0] - other.value[0]) <= 1))


class Point(tuple):

    def __new__(cls: Type[Point], x: int, y: int):
        return tuple.__new__(cls, (x, y))

    @classproperty
    def origin(self: Type[Point]):
        return Point(0, 0)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def xy(self):
        return self[0], self[1]

    @property
    def ij(self):
        return self[1], self[0]

    @property
    def neighbors(self):
        return [self + d for d in Direction]

    def __add__(self, other):
        if isinstance(other, Direction):
            other = other.value
        elif isinstance(other, (Point, Size)):
            pass
        else:
            return NotImplemented
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if isinstance(other, Direction):
            other = other.value
        elif isinstance(other, (Point, Size)):
            pass
        else:
            return NotImplemented
        return Point(self.x - other[0], self.y - other[1])


class Size(tuple):

    def __new__(cls: Type[Size], width: int, height: float):
        assert width >= 0
        assert height >= 0
        return super().__new__(cls, (width, height))

    def __floordiv__(self, n):
        if not isinstance(n, (int, float)):
            return NotImplemented
        assert n > 0
        return Size(self[0] // n, self[1] // n)

    @property
    def width(self):
        return self[0]

    @property
    def height(self):
        return self[1]

    @property
    def area(self):
        return self.width * self.height


class Span(tuple):

    def __new__(cls: Type[Span], start, end):
        return super().__new__(cls, (start, end))

    @property
    def start(self):
        return self[0]

    @property
    def end(self):
        return self[1]

    def __contains__(self, point):
        return self.start <= point <= self.end

    def __iter__(self):
        return iter(range(self.start, self.end+1))

    def __len__(self):
        return self.end - self.start + 1

    def __add__(self, n):
        if isinstance(n, int):
            return Span(self.start + n, self.end + n)
        return NotImplemented

    def __sub__(self, n):
        return self - n

    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start

    def shift_into_view(self, point, *, margin=0):
        if self.start + margin <= point <= self.end - margin:
            return self
        assert isinstance(point, int)
        assert isinstance(margin, int)
        assert margin > 0
        d = (min(0, point - (self.start + margin)) +
             max(0, point - (self.end - margin)))
        return self + d

    def scale(self, width, *, pivot=None):
        old_width = len(self)
        if old_width == width:
            return self
        if pivot is None:
            pivot = (self.start + self.end) // 2

        relative_pos = (pivot - self.start) / old_width
        start_offset = relative_pos * width
        if relative_pos <= 0.5:
            start_offset = int(start_offset + 0.5)
        else:
            start_offset = int(start_offset)

        start = pivot - start_offset
        end = start + width - 1
        return Span(start, end)


class Rect(tuple):

    def __new__(cls: Type[Rect], origin, size):
        return super().__new__(cls, (origin, size))

    @classmethod
    def from_edges(cls, *, top, bottom, left, right):
        return Rect(Point(left, top), Size(right - left + 1, bottom - top + 1))
    
    @classmethod
    def from_spans(cls, *, vertical: Span, horizontal: Span):
        return cls.from_edges(
            top=vertical.start, bottom=vertical.end,
            left=horizontal.start, right=horizontal.end
            )

    @classmethod
    def centered_at(cls, size, center):
        left = center.x - size.width // 2
        top = center.y - size.height // 2
        return Rect(Point(left, top), size)

    @property
    def size(self):
        return self[1]

    @property
    def top_left(self):
        return self[0]

    @property
    def top(self):
        return self.top_left.y

    @property
    def bottom(self):
        return self.top_left.y + self.size.height - 1

    @property
    def left(self):
        return self.top_left.x

    @property
    def right(self):
        return self.top_left.x + self.size.width - 1

    @property
    def width(self):
        return self.size.width

    @property
    def height(self):
        return self.size.height

    @property
    def area(self):
        return self.size.area

    @property
    def indices(self):
        return np.s_[self.top:self.bottom, self.left:self.right]

    @property
    def vertical_span(self):
        return Span(self.top, self.bottom)

    @property
    def horizontal_span(self):
        return Span(self.left, self.right)

    def edge_length(self, edge):
        if edge is Direction.up or edge is Direction.down:
            return self.width
        if edge is Direction.left or edge is Direction.right:
            return self.height
        raise ValueError("Expected an orthogonal direction.")

    def edge_span(self, edge):
        if edge is Direction.up or edge is Direction.down:
            return self.horizontal_span
        if edge is Direction.left or edge is Direction.right:
            return self.vertical_span
        raise ValueError("Expected an orthogonal direction.")

    def edge_point(self, edge, parallel, orthogonal):
        """Return a point, relative to a particular edge.
        `parallel` is the absolute coordinate parallel to the given edge. For
        example, if `edge` is `Direction.top`, then `parallel` is the
        x-coordinate.
        `orthogonal` is the RELATIVE offset from the given edge, towards the
        interior of the rectangle. So for `Direction.top`, the y-coordinate is
        `self.top + orthogonal`.
        """
        if edge is Direction.up:
            return Point(parallel, self.top + orthogonal)
        elif edge is Direction.down:
            return Point(parallel, self.bottom - orthogonal)
        elif edge is Direction.left:
            return Point(parallel, self.left + parallel)
        elif edge is Direction.right:
            return Point(parallel, self.right - parallel)
        raise ValueError("Expected an orthogonal direction.")

    def relative_point(self, relative_width: float, relative_height: float):
        """Find a point x% across the width and y% across the height. The
        arguments should be floats between 0 and 1.
        For example, `relative_point(0, 0)` returns the top left, and
        `relative_point(0.5, 0.5)` returns the center.
        """
        assert 0 <= relative_width <= 1
        assert 0 <= relative_height <= 1
        return Point(
            self.left + int((self.width - 1) * relative_width + 0.5),
            self.top + int((self.height - 1) * relative_height + 0.5),
            )

    @property
    def center(self):
        return self.relative_point(0.5, 0.5)

    def __contains__(self, other):
        if isinstance(other, Rect):
            return (
                self.top <= other.top and
                self.bottom >= other.bottom and
                self.left <= other.left and
                self.right >= other.right
                )
        elif isinstance(other, Point):
            return (
                self.left <= other.x <= self.right and
                self.top <= other.y <= self.bottom
                )
        else:
            return False

    def replace(self, *, top=None, bottom=None, left=None, right=None):
        if top is None:
            top = self.top
        if bottom is None:
            bottom = self.bottom
        if left is None:
            left = self.left
        if right is None:
            right = self.right

        return type(self).from_edges(
            top=top,
            bottom=bottom,
            left=left,
            right=right,
            )

    def shift(self, *, top=0, bottom=0, left=0, right=0):
        return type(self).from_edges(
            top=self.top + top,
            bottom=self.bottom + bottom,
            left=self.left + left,
            right=self.right + right,
            )

    def shrink(self, amount):
        new_left = self.left + amount
        new_right = self.right - amount
        if new_left > new_right:
            new_left = new_right = (self.left + self.right) // 2

        new_top = self.top + amount
        new_bottom = self.bottom - amount
        if new_top > new_bottom:
            new_top = new_bottom = (self.top + self.bottom) // 2

        return type(self).from_edges(
            top=new_top, bottom=new_bottom,
            left=new_left, right=new_right,
            )

    def iter_border(self):
        for x in range(self.left + 1, self.right):
            yield Point(x, self.top), Direction.up
            yield Point(x, self.bottom), Direction.down
        for y in range(self.top + 1, self.bottom):
            yield Point(self.left, y), Direction.left
            yield Point(self.right, y), Direction.right

        yield Point(self.left, self.top), Direction.up_left
        yield Point(self.right, self.top), Direction.up_right
        yield Point(self.left, self.bottom), Direction.down_left
        yield Point(self.right, self.bottom), Direction.down_right

    def iter_points(self):
        for x in range(self.left, self.right + 1):
            for y in range(self.top, self.bottom + 1):
                yield Point(x, y)

    def range_width(self):
        """Iterate over every x-coordinate within the width of the Rect."""
        return range(self.left, self.right + 1)

    def range_height(self):
        """Iterate over every y-coordinate within the height of the Rect."""
        return range(self.top, self.bottom + 1)
