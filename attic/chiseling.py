"""Chiseling algorithm for random paths.

https://www.boristhebrave.com/2018/04/28/random-paths-via-chiseling/
"""
from __future__ import annotations
from typing import Callable, List, Tuple, TypeVar, Generic, Optional

import random
import math
import numpy as np
from collections import defaultdict

DType = TypeVar("DType")
U = TypeVar("U")
V = TypeVar("V")
R = TypeVar("R")


class Array(np.ndarray, Generic[DType]):
    """Dummy class for type annotating NumPy ndarrays."""




class Graph:

    def __init__(self, vertices) -> None:
        self.vertices = vertices
        self.graph = defaultdict([list])
        self.time = 0

    def add_edge(self, u, v) -> None:
        self.graph[u].append(v)
        self.graph[v].append(u)

    def find_articulation_points(self, u, visited, ap, parent, low, disc):
        children = 0
        visited[u] = True
        disc[u] = self.time
        low[u] = self.time
        self.time += 1

        for v in self.graph[u]:
            if not visited[v]:
                parent[v] = u
                children += 1
                self.find_articulation_points(v, visited, ap, parent, low, disc)
                low[u] = min(low[u], low[v])
                if parent[u] == -1 and children > 1:
                    ap[u] = True
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    def traverse(self):
        visited = [False] * self.vertices
        disc = [float("Inf")] * self.vertices
        low = [float("Inf")] * self.vertices
        parent = [-1] * self.vertices
        ap_list = [False] * self.vertices

        for i in range(self.vertices):
            if not visited[i]:
                self.find_articulation_points(i, visited, ap_list, parent, low, disc)
        return ap_list


class ChiselingAlgorithm:

    def __init__(self) -> None:
        self.neighbors = [(  1,  0 ),
                          (  0,  1 ),
                          ( -1,  0 ),
                          (  0, -1 )]

    def find_articulation_points(
            self,
            width: int,
            height: int,
            walkable: Array[np.bool],
            relevant: Optional[Array[np.bool]] = None,
        ) -> np.ndarray:
        """Finds the articulation points of a 2D Array.

        The cells that, if they were marked as unwalkable, would split the
        remaining cells into separate components (i.e. untraversable).
        If `relevant` is supplied,, then we only return an articulation point
        if it would split the relevant cells apart. Relevant cells are always
        articulation points.
        """
        shape: Tuple[int, int] = width, height
        low: Array[np.int32] = np.zeros(shape, dtype=np.int32, order="F")
        dfs_num: Array[np.int32] = np.zeros(shape, dtype=np.int32, order="F")
        is_articulation: Array[np.bool] = np.zeros(shape, dtype=np.bool, order="F")

        def cut_vertex(ux: int, uy: int) -> Tuple[int, bool]:
            child_count = 0
            is_relevant = np.any(relevant) and relevant[ux][uy]
            if is_relevant:
                is_articulation[ux][uy] = True
            is_relevant_subtree = is_relevant

            num: int = 1
            low[ux][uy] = dfs_num[ux][uy] = num
            num += 1
            print(num)

            for (dx, dy) in self.neighbors:
                vx = ux + dx
                vy = uy + dy

                if vx < 0 or vx >= width or vy < 0 or vy >= height:
                    continue
                if not walkable[vx][vy]:
                    continue

                unvisited = not dfs_num[vx][vy]
                if unvisited:
                    _, child_relevant_subtree = cut_vertex(vx, vy)
                    child_count += 1
                    if child_relevant_subtree:
                        is_relevant_subtree = True
                    if low[vx][vy] >= dfs_num[ux][uy]:
                        if not np.any(relevant) or child_relevant_subtree:
                            is_articulation[ux][uy] = True
                    low[ux][uy] = min(low[ux][uy], low[vx][vy])
                else:
                    low[ux][uy] = min(low[ux][uy], dfs_num[vx][vy])
            return child_count, is_relevant_subtree

        for x in range(width-1):
            for y in range(height-1):
                if not walkable[x][y]:
                    continue
                if np.any(relevant) and not relevant[x][y]:
                    continue
                child_count, child_relevant_subtree = cut_vertex(x, y)
                is_articulation[x][y] = child_count > 1 or not not np.any(relevant)
                return is_articulation
        return is_articulation


    def choose_random(
            self,
            weights: Array[np.int],
            rand_func: Optional[Callable[[], int]] = None
        ) -> Optional[int]:
        _random = rand_func if rand_func else random.random

        total_weight: int = 0
        for i, _ in enumerate(weights):
            total_weight += weights[i]
        if total_weight <= 0:
            return None

        r = _random() * total_weight

        try:
            for i, _ in enumerate(weights):
                r -= weights[i]
                if r < 0:
                    return i
        except:
            raise ValueError("Failed to choose a random point.")

    def choose_random_point(
        self,
        width: int,
        height: int,
        weights: Array[np.int],
        rand_func: Optional[Callable[[], int]] = None
        ) -> Optional[int]:
        linear_weights = []
        for x in range(width):
            for y in range(height):
                linear_weights.append(weights[x][y])
        i = self.choose_random(linear_weights, rand_func)
        if not i:
            return None
        return [math.floor(i / height), i % height]

    def map_2D(
            self,
            width: int,
            height: int,
            values: Array[U],
            func: Callable[[U], R]
        ) -> Array[R]:
        results: Array[R] = np.array((width, height), order="F")
        for x in range(width):
                results[x] = func(values[x])
        return results

    def zip_map_2D(
            self,
            width: int,
            height: int,
            vals_a: Array[U],
            vals_b: Array[V],
            func: Callable[[U, V], R]
        ) -> Array[R]:
        results: Array[R] = np.zeros((width, height), order="F")
        for x in range(width):
            for y in range(height):
                results[x][y] = func(vals_a[x][y], vals_b[x][y])
        return results

    def random_path(
            self,
            width: int,
            height: int,
            walkable: Array[np.bool],
            points: Array[np.bool],
            random: Optional[Callable[[], int]] = None
        ) -> Array[np.bool]:
        path: Array[np.bool] = np.zeros((width, height), dtype=np.bool, order="F")
        path[:] = walkable[:]
        while True:
            art_points = self.find_articulation_points(width, height, path, points)
            func = (lambda is_path, is_art_point : 1.0 if is_path and not is_art_point else 0.0)
            weights = self.zip_map_2D(width, height, path, art_points, func)
            chisel_point = self.choose_random_point(width, height, weights, random)
            if not chisel_point:
                break
            (x, y) = chisel_point
            path[x][y] = False
        return path

    def random_connected_set(
            self,
            width: int,
            height: int,
            walkable: Array[np.bool],
            count: int,
            random: Optional[Callable[[], int]]
        ) -> Array[np.bool]:
        pass


if __name__ == '__main__':
    width = 32  # over 30 and it gets a recursion error lol
                # I'll have to do it in chunks, ideally of 16x16
    w = np.zeros((width, width), dtype=np.bool, order="F")
    w[:] = True
    chiseling = ChiselingAlgorithm()
    points = np.zeros((width, width), dtype=np.bool, order="F")
    points[0][0] = True
    points[width-1][width-1] = True
    result = chiseling.random_path(width, width, w, points)
    print(result)
