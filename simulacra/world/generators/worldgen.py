from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List

import numpy as np

from simulacra.utils.map_grid import Array
from simulacra.utils.geometry import Point

WORLD_WIDTH = 200
WORLD_HEIGHT = 80

@dataclass
class RegionCell:
    """Worldmap representation of a single Region."""

    height: int
    temperature: int
    precipitation: int
    drainage: int
    biome: int

    has_river: bool = False
    is_settled: bool = False

    biome_id: int = 0
    prosperity: int = 0


@dataclass
class Species:
    name: str
    preferred_biome: int
    strength: int
    size: int
    fertility: int
    aggression: int
    form: int


@dataclass
class CultureSite:
    x: int
    y: int
    category: int
    suitable: bool
    population_cap: int

    population: int = 0
    is_capital: bool = False


@dataclass
class Culture:
    name: str
    species: Species
    government: Government
    color: int

    sites: List[CultureSite] = []
    suitable_sites: List[CultureSite] = []
    total_population: int = 0

    @property
    def aggression(self) -> int:
        return self.species.aggression + self.government.aggression


@dataclass
class Government:
    name: str
    description: str
    aggression: int
    militarization: int
    tech_bonus: int


def point_distance_round(a: Point, b: Point):
    return round(abs(b.x - a.x) + abs(b.y - a.y))


def lowest_neighbor(x: int, y: int, world: Array[int]):
    min_val: int = 1
    x: int = 0
    y: int = 0



world = [[0 for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
