from __future__ import annotations
from typing import Callable, List, Optional, Tuple, Union

import math
import numpy as np
import random
import pymunk
import tcod

from aabbtree import AABB, AABBTree
from . import vector
from config import STAGE_WIDTH, STAGE_HEIGHT
from geometry import *
from room import Room

    
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
    
    
class Node:
    
    def __init__(
            self,
            uid: str,
            position: Union[Tuple[int, int], Node],
            width: int,
            height: int
        ) -> None:
        if isinstance(position, Node):
            self.x = position.x
            self.y = position.y
        else:
            self.x = position[0]
            self.y = position[1]
        self.uid = uid
        self.width = width
        self.height = height
        self.parent = None
        self.children = []
        
        self.x1 = self.x
        self.y1 = self.y
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height
        
    @property
    def center(self) -> Tuple[int, int]:
        """Return the index for the node's center coordinate."""
        return ((self.x + (self.x + self.width)) // 2, 
                (self.y + (self.y + self.height)) // 2)
    
    def distance_to(self, other: Node) -> float:
        """Return an approximate distance from this node to another."""
        x, y = self.center
        other_x, other_y = other.center
        return abs(other_x - x) + abs(other_y - y)
    
    def intersects(self, other: Node) -> bool:
        """Return True if this node intersects with another."""
        return (
            self.x1 <= other.x2 and
            self.x2 >= other.x1 and
            self.y1 <= other.y2 and
            self.y2 >= other.y1
            )
        
    def add_child(self, node: Node) -> None:
        self.children.append(node)
        node.parent = self
        
    def remove_child(self, node: Node) -> None:
        self.children.remove(node)


class GraphGenerator:
    
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.nodes = []
        self.map_data = np.zeros((256, 256), dtype=np.int)
    
    def generate_rooms(self) -> None:
        for node in self.nodes:
            room = Room(node.x, node.y, node.width, node.height)
            self.map_data[room.inner] = 1
            self.map_data[room.outer] = 2
    
    def generate_nodes_in_radius(
            self,
            max_nodes: int, 
            min_size: int,
            max_size: int, 
            placement_radius: int,
            placement_function=None
        ) -> None:
        for i in range(max_nodes):
            x, y = self.get_random_points_in_circle(placement_radius)
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            new_node = Node(str(i), (x, y), w, h)
            self.nodes.append(new_node)

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
    
    def cartesian_to_polar(self, x: int, y: int):
        pass