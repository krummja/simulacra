"""Area Generation"""

from __future__ import annotations
from typing import Callable, List, Optional, Tuple, Union

import random
import math
import numpy as np

from engine.apparata.node import Node
from engine.apparata.graph import Graph, GraphQuery

from engine.geometry import Rect


class Vector:

    def __init__(self, *args) -> None:
        if len(args) == 1:
            self._vector = np.array(args[0])
        elif len(args) == 2:
            self._vector = np.array([args[0], args[1]])

    @property
    def x(self) -> float:
        return self._vector[0]

    @property
    def y(self) -> float:
        return self._vector[1]

    @x.setter
    def x(self, value: int) -> None:
        self._vector[0] = value

    @y.setter
    def y(self, value: int) -> None:
        self._vector[1] = value

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

    @property
    def ij(self) -> Tuple[float, float]:
        return self.y, self.x


class WorldNode(Node):
    """Graph WorldNode"""

    def __init__(
            self,
            uid: str,
            position: Union[Tuple[int, int], WorldNode],
            width: int,
            height: int,
            rect: Optional[Rect] = None
        ) -> None:
        if isinstance(position, WorldNode):
            self.x = position.x
            self.y = position.y
        else:
            self.x = position[0]
            self.y = position[1]

        super().__init__(uid, label=(self.x, self.y))

        self.width = width
        self.height = height
        self.parent = None
        self.children = []
        self.rect = rect

    @property
    def x1(self):
        return self.x

    @property
    def y1(self):
        return self.y

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height

    @property
    def center(self) -> Tuple[int, int]:
        """Return the index for the node's center coordinate."""
        return ((self.x + (self.x + self.width)) // 2,
                (self.y + (self.y + self.height)) // 2)

    def distance_to(self, other: WorldNode) -> float:
        """Return an approximate distance from this node to another."""
        x, y = self.center
        other_x, other_y = other.center
        return abs(other_x - x) + abs(other_y - y)

    def intersects(self, other: WorldNode) -> bool:
        """Return True if this node intersects with another."""
        return (
            self.x1 <= other.x2 and
            self.x2 >= other.x1 and
            self.y1 <= other.y2 and
            self.y2 >= other.y1
            )

    def add_child(self, node: WorldNode) -> None:
        self.children.append(node)
        node.parent = self

    def remove_child(self, node: WorldNode) -> None:
        self.children.remove(node)


class GraphGenerator:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.world_nodes = []
        self.map_data = np.zeros((256, 256), dtype=np.int)
        self.graph = Graph()
        self.query = GraphQuery(self.graph)

    def generate_nodes_in_radius(
            self,
            max_nodes: int,
            min_size: int,
            max_size: int,
            placement_radius: int,
        ) -> None:
        for i in range(max_nodes):
            x, y = self.get_random_points_in_circle(placement_radius)
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            new_node = WorldNode(str(i), (x, y), w, h)
            self.world_nodes.append(new_node)

    def get_random_points_in_circle(self, placement_radius: int) -> Tuple[int, int]:
        """Generate a random point within a circle defined by `placement_radius`.
        Returns an integer tuple used to fix the position of a graph node.
        """
        t = 2 * math.pi * random.random()
        u = random.random() * random.random()
        r = 2 - u if u > 1 else u
        x = int(placement_radius * r * math.cos(t) + (self.width // 2))
        y = int(placement_radius * r * math.sin(t) + (self.height // 2))
        return x, y

    def polar_to_cartesian(self, radius: float, theta: float) -> Tuple[float, float]:
        """Convert polar coordinates to cartesian coordinates."""
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        return x, y

    def add_world_node(
            self,
            uid: str,
            position: Union[Tuple[int, int], WorldNode],
            width: int,
            height: int,
            rect: Optional[Rect] = None
        ) -> None:
        new_node = WorldNode(uid, position, width, height, rect)
        self.world_nodes.append(new_node)
        self.graph.add_node(new_node)