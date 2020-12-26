from __future__ import annotations
from typing import Tuple

import math
import numpy as np
import random
import aabbtree as abt
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
    
    def __init__(self, x: int, y: int, width: int, height: int, uid: str) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
        self.uid = uid
        
    @property
    def x(self) -> int:
        return self.x1
    
    @property
    def y(self) -> int:
        return self.y1
        
    @x.setter
    def x(self, value: int) -> None:
        self.x1 = value
        self.x2 = value + self.width
        
    @y.setter
    def y(self, value: int) -> None:
        self.y1 = value
        self.y2 = value + self.height
        
    @property
    def x_half(self) -> Tuple[int, int]:
        return (self.width / 2), 0.0
    
    @property
    def y_half(self) -> Tuple[int, int]:
        return 0.0, (self.height / 2)
    
    @property
    def center(self) -> Tuple[int, int]:
        """Return the index for the node's center coordinate."""
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2
    
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


class GraphGenerator:
    
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.nodes = []
    
    def generate(
            self, 
            max_nodes: int, 
            min_size: int, 
            max_size: int, 
            radius: int
        ) -> None:
        debug_map = self.generate_nodes(max_nodes, min_size, max_size, radius)
        self.separate_nodes()
        
        return debug_map
    
    def generate_nodes(
            self,
            max_nodes: int, 
            min_size: int,
            max_size: int, 
            placement_radius: int
        ) -> None:
        for _ in range(max_nodes):
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            x, y = self.get_random_points_in_circle(placement_radius)
            new_node = Node(x, y, w, h, f'{_}')
            self.nodes.append(new_node)
            
        room_map = np.zeros((300, 300), dtype=np.int)
        for node in self.nodes:
            debug_room = Room(node.x, node.y, node.width, node.height)
            room_map[debug_room.outer] = 1
            room_map[debug_room.inner] = 2
        return room_map

    def generate_rooms(self) -> np.ndarray:
        room_map = np.zeros((300, 300), dtype=np.int)
        for node in self.nodes:
            new_room = Room(node.x, node.y, node.width, node.height)
            room_map[new_room.outer] = 1
            room_map[new_room.inner] = 2
        return room_map
    
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

    def separate_nodes(self) -> None:
        for node in self.nodes:
            separation = self.compute_separation(node)
            node.x += int(separation.x)
            node.y += int(separation.y)
    
    def compute_separation(self, agent: Node) -> Tuple[int, int]:
        force: Vector = Vector(0, 0)
        neighbors: int = 0
        
        for node in self.nodes:
            if node != agent:
                if agent.intersects(node):
                    force = self.minimum_translation_vector(force, agent, node)
                    neighbors += 1
        if neighbors == 0:
            return force

        # force.x /= neighbors
        # force.y /= neighbors
        force.x *= -1
        force.y *= -1
        return force
        
    def minimum_translation_vector(self, force: Vector, agent: Node, node: Node) -> Vector:
        y1 = max(agent.y1, node.y1)
        y2 = min(agent.y2, node.y2)
        width = max(y1, y2) - min(y1, y2)
        
        x1 = max(agent.x1, node.x1)
        x2 = min(agent.x2, node.x2)
        height = max(x1, x2) - min(x1, x2)
        
        # if width < height:
        #     force.x, force.y = 0, width
        # elif width > height:
        #     force.x, force.y = height, 0
        # else:
        #     force.x, force.y = height, width

        force.x, force.y = height, width

        return force

    def normalize_vector(self, vec: Vector, axis=-1, order=2) -> Vector:
        l2 = np.atleast_1d(np.linalg.norm(vec._vector, order, axis))
        l2[l2==0] = 1
        vec = (vec._vector / np.expand_dims(l2, axis)).ravel()
        return Vector(vec)