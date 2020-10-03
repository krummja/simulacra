from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from engine.items import Item
from content.tiles import font_map

if TYPE_CHECKING:
    from engine.location import Location


class OpenableState:

    def __init__(self: OpenableState):
        self._is_open: bool = False
        self.state: str = "closed"

    @property
    def is_open(self: OpenableState) -> bool:
        return self._is_open

    @is_open.setter
    def is_open(self: OpenableState, value: bool) -> None:
        self._is_open = value


class Door(Item, OpenableState):

    closed_sprite: int = font_map['door_01']
    open_sprite: int = font_map['door_02']

    def __init__(
            self: Door,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            passable: bool,
            equippable: bool
        ) -> None:
        Item.__init__(
            self,
            char,
            color,
            bg,
            noun_text,
            location,
            passable,
            equippable
            )
        OpenableState.__init__(self)
        self.location.area.tiles[self.location.x, self.location.y]["transparent"] = False

    def mut_state(self: Door) -> None:
        if self.is_open is True:
            self.is_open = False
            self.state = "closed"
            self.passable = False
            self.location.area.model.report(f"{self.noun_text} swings shut.")
            self.location.area.tiles[self.location.x, self.location.y]["transparent"] = False
            self.location.area.update_fov()
            self.char = self.closed_sprite
        elif self.is_open is False:
            self.is_open = True
            self.state = "open"
            self.passable = True
            self.location.area.model.report(f"{self.noun_text} creaks open.")
            self.location.area.tiles[self.location.x, self.location.y]["transparent"] = True
            self.location.area.update_fov()
            self.char = self.open_sprite

    def plan_activate(self: Door, action):
        return action
