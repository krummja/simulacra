"""ENGINE.GEOMETRY.Rect"""
from __future__ import annotations

from typing import Generator, Optional, Type, Union

import numpy as np

from .vector import vector2
from .direction import Direction
from .point import Point
from .size import Size
from .span import Span


def clamp(number, low, high):
    return max(low * 1.0, min(number * 1.0, high * 1.0))


class Rect(tuple):
    """Representation of a Rectangle."""

    def __new__(cls: Type[Rect], origin, size) -> Rect:
        return super().__new__(cls, (origin, size))

    @classmethod
    def from_edges(cls, *, top: int, bottom: int, left: int, right: int) -> Rect:
        """Constructor method.

        Create a new Rect object by defining the values of its four edges.
        """
        return Rect(Point(left, top), Size(right - left + 1, bottom - top + 1))

    @classmethod
    def from_spans(cls, *, vertical: Span, horizontal: Span) -> Rect:
        """Constructor method.

        Create a new Rect object by defining its vertical and horizontal
        dimensions as Span objects.
        """
        return cls.from_edges(
            top=vertical.start, bottom=vertical.end,
            left=horizontal.start, right=horizontal.end
            )

    @classmethod
    def centered_at(cls, size: Size, center: Point) -> Rect:
        """Constructor method.

        Create a new Rect object by defining its dimensions as a Size object
        and its centerpoint as a Point object.
        """
        left = center.x - size.width // 2
        top = center.y - size.height // 2
        return Rect(Point(left, top), size)

    @property
    def size(self) -> Size:
        """Return this Rect's Size definition."""
        return self[1]

    @property
    def top_left(self) -> Point:
        """Return this Rect's top-left Point definition."""
        return self[0]

    @property
    def top(self) -> int:
        return self.top_left.y

    @property
    def bottom(self) -> int:
        return self.top_left.y + self.size.height - 1

    @property
    def left(self) -> int:
        return self.top_left.x

    @property
    def right(self) -> int:
        return self.top_left.x + self.size.width - 1

    @property
    def width(self) -> int:
        return self.size.width

    @property
    def height(self) -> int:
        return self.size.height

    @property
    def area(self) -> int:
        """Getter for the area property of this Rect's Size definition."""
        return self.size.area

    @property
    def inner(self) -> np.IndexExpression:
        """Get a NumPy IndexExpression for the inner portion of the Rect."""
        return np.s_[(self.left+1):self.right-1, (self.top+1):self.bottom-1]

    @property
    def outer(self) -> np.IndexExpression:
        """Get a NumPy IndexExpression for the inner portion + the border
        of the Rect.
        """
        return np.s_[self.left:(self.right+1), self.top:(self.bottom+1)]

    @property
    def indices(self) -> np.IndexExpression:
        """Get a NumPy IndexExpression for this Rect."""
        return np.s_[self.top:self.bottom, self.left:self.right]

    @property
    def vertical_span(self) -> Span:
        """Return a Span for this Rect's vertical axis."""
        return Span(self.top, self.bottom)

    @property
    def horizontal_span(self) -> Span:
        """Return a Span for this Rect's horizontal axis."""
        return Span(self.left, self.right)

    def distance_to(self, other: Rect) -> float:
        """Return an approximate distance from this rect to another."""
        x, y = self.center
        other_x, other_y = other.center
        return abs(other_x - x) + abs(other_y - y)

    def edge_length(self, edge: Direction) -> int:
        """Use a Direction to get the length of the relevant edge."""
        if edge is Direction.up or edge is Direction.down:
            return self.width
        if edge is Direction.left or edge is Direction.right:
            return self.height
        raise ValueError("Expected an orthogonal Direction.")

    def edge_span(self, edge: Direction) -> Span:
        """Use a Direction to get a Span that starts and ends at
        opposite edges and crosses the centerpoint of this Rect."""
        if edge is Direction.up or edge is Direction.down:
            return self.horizontal_span
        if edge is Direction.left or edge is Direction.right:
            return self.vertical_span
        raise ValueError("Expected an orthogonal Direction.")

    def edge_point(self, edge: Direction, parallel: int, orthogonal: int) -> Point:
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

    def relative_point(self, relative_width: float, relative_height: float) -> Point:
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
    def center(self) -> Point:
        """Get the center of this Rect as a Point object."""
        return self.relative_point(0.5, 0.5)

    def replace(self, *,
            top: Optional[int] = None,
            bottom: Optional[int] = None,
            left: Optional[int] = None,
            right: Optional[int] = None
        ) -> Rect:
        """Get a new Rect derived from this one, optionally defined in terms
        of edge values. Providing values ot this method pass them as arguments
        to `Rect.from_edges()` constructor.

        Leave a parameter unfilled to get the current Rect's value for that
        parameter, or provide an integer to override.
        """
        if top is None:
            top = self.top
        if bottom is None:
            bottom = self.bottom
        if left is None:
            left = self.left
        if right is None:
            right = self.right
        return type(self).from_edges(top=top, bottom=bottom, left=left, right=right)

    def shift(self, *,
            top: int = 0,
            bottom: int = 0,
            left: int = 0,
            right: int = 0
        ) -> Rect:
        """Get a new Rect derived from this one, defined as offsets from the
        current Rect's values. The values provided for this method's parameters
        are passed to `Rect.from_edges()` constructor."""
        return type(self).from_edges(
            top=self.top + top,
            bottom=self.bottom + bottom,
            left=self.left + left,
            right=self.right + right,
            )

    def shrink(self, amount: int) -> Rect:
        """Get a new Rect derived from this one, defined as an integer offset
        applied to all sides."""
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

    def iter_border(self) -> Generator:
        """Return Points for every x,y in the border of the Rect as well as
        a Direction object encoding the side of the given edge.

        Returns diagonal Directions for the corners of the Rect."""
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

    def iter_points(self) -> Generator:
        for x in range(self.left, self.right + 1):
            for y in range(self.top, self.bottom + 1):
                yield Point(x, y)

    def range_width(self):
        """Iterate over every x-coordinate within the width of the Rect."""
        return range(self.left, self.right + 1)

    def range_height(self):
        """Iterate over every y-coordinate within the height of the Rect."""
        return range(self.top, self.bottom + 1)

    def intersects(self, other: Rect) -> bool:
        """Returns True if this Rect overlaps with another at any point."""
        return (
            self.top <= other.bottom and
            self.bottom >= other.top and
            self.left <= other.right and
            self.right >= other.left
            )

    @property
    def edge_normals(self):
        return [vector2(0, -1), vector2(1, 0), vector2(0, 1), vector2(-1, 0)]

    @property
    def vertices(self):
        return [vector2(self.left, self.bottom),
                vector2(self.left, self.top),
                vector2(self.right, self.top),
                vector2(self.right, self.bottom)]

    def get_support(self, direction: np.ndarray):
        best_projection = -float('inf')
        for i in range(3):
            v = self.vertices[i]
            projection = direction.dot(v)
            if projection > best_projection:
                best_vertex = v
                best_projection = projection
        return best_vertex

    def least_penetration_axis(self, other: Rect):
        best_distance = -float('inf')
        best_index = 0
        for i in range(3):
            n = self.edge_normals[i]
            s = other.get_support(-n)
            v = self.vertices[i]
            d = n.dot(s - v)
            if d > best_distance:
                best_distance = d
                best_index = i
        face_index = best_index
        return face_index, int(best_distance)

    def separate_from(self, other: Rect):
        attempts = 300
        A = self
        B = other
        A_x = self.center[0]
        A_y = self.center[1]
        B_x = other.center[0]
        B_y = other.center[1]
        while A.intersects(B) and attempts > 0:
            face, distance = self.least_penetration_axis(other)
            direction = self.edge_normals[face]
            A_x += int(direction[0] * int(distance))
            A_y += int(direction[1] * int(distance))
            B_x -= int(direction[0] * int(distance))
            B_y -= int(direction[1] * int(distance))
            attempts -= 1
            A = self.replace(left=A_x, right=A_x+(self.width//2), top=A_y, bottom=A_y+(self.height//2))
            B = other.replace(left=B_x, right=B_x+(other.width//2), top=B_y, bottom=B_y+(other.height//2))
        return A, B

    def clamp(self, x: int, y: int):
        x = clamp(x, min(self.left,   self.left   + self.width  ),
                     max(self.right,  self.right  + self.width  ))
        y = clamp(y, min(self.top,    self.top    + self.height ),
                     max(self.bottom, self.bottom + self.height ))
        return int(x), int(y)

    def __contains__(self, other: object) -> bool:
        """Check if this Rect _properly_ contains a target Rect or Point."""
        if isinstance(other, Rect):
            return (
                self.top < other.top and
                self.bottom > other.bottom and
                self.left < other.left and
                self.right > other.right
                )
        elif isinstance(other, Point):
            return (
                self.left <= other.x <= self.right and
                self.top <= other.y <= self.bottom
                )
        else:
            return False
