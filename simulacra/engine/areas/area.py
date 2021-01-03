"""Define an area of the game. Includes models for different data structures
representing elements contained in the area.

Classes:

    ActorModel
    Area
    AreaLocation
    AreaModel
    ItemModel
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Set, Tuple, Optional

import numpy as np
from engine.areas.location import Location
from engine.geometry import Point
from engine.rendering.camera import Camera
from engine.tiles.tile import tile_dt, tile_graphic

if TYPE_CHECKING:
    from engine.entities import Item, Player
    from engine.entities.entity import Entity
    from engine.events import Actor
    from engine.model import Model


class AreaModel:
    """Model class that holds the actual data structures for a given area."""

    def __init__(self, area: Area) -> None:
        self.area = area
        self.uid = "<unset>"
        self.shape = self.area.shape
        self.tiles = np.zeros(self.shape, dtype=tile_dt)
        self.effects = np.zeros(self.shape, dtype=tile_graphic)
        self.explored = np.zeros(self.shape, dtype=bool)
        self.visible = np.zeros(self.shape, dtype=bool)

    def get_bg_color(self, x: int, y: int) -> List[int]:
        cam_x, cam_y = self.area.camera.get_camera_pos()
        target_x, target_y = x + cam_x, y + cam_y
        target_tile = self.tiles[target_y, target_x]
        return list(target_tile[2][2][0:3])


class ActorModel:
    """Model class that holds references to all of the area's actors.

    Actors are stored in a set; there shouldn't be a reason to directly access
    an actor in the game. Accessing the owning entity via the Model is usually
    sufficient.
    """

    def __init__(self, area: Area) -> None:
        self.area = area
        self.actors: Set[Actor] = set()

    def register_actor(self, actor: Actor) -> None:
        self.actors.add(actor)


class ItemModel:
    """Model class that holds references to all of an area's items.

    Items are stored in arrays representing a tile in the area, keyed to a
    tuple that encodes the area location of that tile.

    items = { (10, 10): [<Item1>, <Item2>, <Item3>] }
    """

    def __init__(self, area: Area) -> None:
        self.area = area
        self.items: Dict[Tuple[int, int], List[Item]] = {}
        self.nearby_items: List[List[Item]] = []

    def __getitem__(self, key: Tuple[int, int]) -> List[Item]:
        """Return a list of items at a given y,x position."""
        return self.items[key]

    def get_nearby(self) -> None:
        """Return a list of items in all neighboring tiles around the player."""
        self.nearby_items.clear()
        for position in Point(*self.area.model.player.location.xy).neighbors:
            try:
                if self.items[position[0], position[1]]:
                    self.nearby_items.append(self.items[position])
            except KeyError:
                continue


class AreaLocation(Location):
    """Representation of a `Location` bound to a specific `Area`."""

    def __init__(self, area: Area, x: int, y: int):
        self.area = area
        self.x = x
        self.y = y


class Area:
    """Base class for defining new areas of the game."""

    def __init__(self, model: Model, width: int, height: int) -> None:
        self._player: Optional[Player] = None
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

    @property
    def items(self) -> Dict[Tuple[int, int], List[Item]]:
        return self.item_model.items

    @property
    def nearby_items(self) -> List[List[Item]]:
        return self.item_model.nearby_items

    def nearby_actor_entities(
            self,
            x: int,
            y: int
        ) -> Entity:
        entity_dict = {}
        for ent in self.actor_model.actors:
            owner: Entity = ent.owner
            entity_dict[owner.location.y, owner.location.x] = owner
        try:
            return entity_dict[y, x]
        except KeyError:
            pass

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
