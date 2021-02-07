from __future__ import annotations


class Structure:

    def __init__(self) -> None:
        self.build_floor()
        self.build_size()

    def build_floor(self):
        raise NotImplementedError

    def build_size(self):
        raise NotImplementedError


class Shop(Structure):

    def build_floor(self):
        self.floor = "wood"

    def build_size(self):
        self.size = (10, 10)


def construct_structure(cls):
    structure = cls()
    structure.build_floor()
    structure.build_size()
    return structure
