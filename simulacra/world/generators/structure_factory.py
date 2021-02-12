from __future__ import annotations
from typing import Tuple
import numpy as np
from enum import Enum
from simulacra.utils.geometry import Rect


class Floor(Enum):
    WOOD = 0
    STONE = 1
    BRICK = 2

class Wall(Enum):
    WOOD = 0
    STONE = 1
    BRICK = 2


class Structure:

    def __init__(self) -> None:
        self.build_walls()
        self.build_floor()
        self.build_size()

    def build_walls(self) -> None:
        raise NotImplementedError

    def build_floor(self) -> None:
        raise NotImplementedError

    def build_size(self) -> None:
        raise NotImplementedError


class Shop(Structure):

    def build_walls(self):
        self.walls = Wall.WOOD

    def build_floor(self):
        self.floor = Floor.STONE

    def build_size(self):
        self.size = (10, 10)

    def construct(self, at: Tuple[int, int]):
        rect = Rect.from_edges(left=at[0],
                               top=at[1],
                               right=at[0] + self.size[0],
                               bottom=at[1] + self.size[1])

        struct = np.zeros(self.size, dtype=int, order="F")
        struct[rect.inner] = 1
        struct = np.pad(struct, pad_width=1, mode='constant', constant_values=0)

        result = np.zeros(struct.shape, dtype=int, order="F")

        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        indices = np.where(struct)
        targets = list(zip(indices[0], indices[1]))

        for (ux, uy) in targets:
            bitsum = 0
            for (dx, dy) in neighbors:
                vx = ux + dx
                vy = uy + dy
                offset = (lambda t : t << neighbors.index((dx, dy)))
                bitsum += offset(struct[vx][vy])

            result[ux-1][uy-1] = bitsum
        return result[0:self.size[0], 0:self.size[1]], rect


def construct_structure(cls, at):
    structure = cls()
    structure, context = structure.construct(at)
    return structure, context
