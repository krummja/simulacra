from __future__ import annotations
from typing import Dict, Tuple, List, Set, TYPE_CHECKING

import numpy as np

from camera import Camera
from location import Location
from tile import tile_dt

if TYPE_CHECKING:
    from actor import Actor
    from item import Item
    from model import Model
    from player import Player


class AreaModel:

    ident: str = '<unset>'

    def __init__(self, area: Area) -> None:
        self.area = area
        self.shape = self.area.shape
        self.tiles = np.zeros(self.shape, dtype=tile_dt)
        self.explored = np.zeros(self.shape, dtype=bool)
        self.visible = np.zeros(self.shape, dtype=bool)

    def get_bg_color(self, x: int, y: int) -> List[int]:
        cam_x, cam_y = self.area.camera.get_camera_pos()
        target_x, target_y = x + cam_x, y + cam_y
        target_tile = self.tiles[target_y, target_x]
        return list(target_tile[2][1][0:3])


class ActorModel:

    def __init__(self, area: Area) -> None:
        self.area = area
        self.actors: Set[Actor] = set()


class ItemModel:
    """Model class that holds references to all of an area's items."""

    def __init__(self, area: Area) -> None:
        self.area = area
        self.items: Dict[Tuple[int, int], List[Item]] = {}

    def __getitem__(self, key: Tuple[int, int]) -> List[Item]:
        """Return a list of items at a given x,y position."""
        return self.items[key]


class AreaLocation(Location):

    def __init__(self, area: Area, x: int, y: int):
        self.area = area
        self.x = x
        self.y = y


class Area:

    _player: Player = None

    def __init__(self, model: Model, width: int, height: int) -> None:
        self.model = model
        self.width = width
        self.height = height
        self.shape: Tuple[int, int] = height, width

        self.area_model = AreaModel(self)
        self.actor_model = ActorModel(self)
        self.item_model = ItemModel(self)
        self.camera = Camera(self)

    @property
    def player(self) -> Player:
        return self._player

    @player.setter
    def player(self, value: Player) -> None:
        self._player = value

    def is_blocked(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        if not self.area_model.tiles[y, x]["move_cost"]:
            return True
        if any(actor.location.xy == (x, y) for actor in self.actor_model.actors):
            return True
        return False

    def __getitem__(self, key: Tuple[int, int]) -> AreaLocation:
        return AreaLocation(self, *key)
