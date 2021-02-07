from __future__ import annotations
from enum import Enum


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
        self.build_floor()
        self.build_size()

    def build_floor(self) -> None:
        raise NotImplementedError

    def build_size(self) -> None:
        raise NotImplementedError


class Shop(Structure):

    def build_floor(self):
        self.floor = Floor.STONE

    def build_size(self):
        self.size = (10, 10)


def construct_structure(cls):
    structure = cls()
    structure.build_floor()
    structure.build_size()
    return structure
