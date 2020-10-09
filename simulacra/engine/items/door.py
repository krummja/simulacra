from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

from content.tiles import font_map
from engine.items import Item
from engine.components.physics import Physics

if TYPE_CHECKING:
    from engine.actions import ActionWithItem
    from engine.location import Location


class OpenableState:

    closed_sprite: Optional[int]
    open_sprite: Optional[int]

    def __init__(self: OpenableState):
        self._is_open: bool = False

    @property
    def is_open(self: OpenableState) -> bool:
        return self._is_open

    @is_open.setter
    def is_open(self: OpenableState, value: bool) -> None:
        self._is_open = value

    def action_activate(self: OpenableState, action: ActionWithItem) -> None:
        pass


class Door(Item, OpenableState):

    def __init__(self: Door, location: Location) -> None:
        Item.__init__(self, location)
        OpenableState.__init__(self)
        self.components['PHYSICS'] = Physics(self, -1)
        self.interactive = True
        self.suffix = "(closed)"

        self.x = self.location.x
        self.y = self.location.y
        self.location.area.tiles[self.y, self.x]["transparent"] = False
        self.location.area.tiles[self.y, self.x]["move_cost"] = 0
        self.open_sprite = font_map['door_01']
        self.closed_sprite = font_map['door_02']

    def plan_activate(self: Door, action):
        return action

    def action_activate(self: Door, action: ActionWithItem) -> None:
        self.char = self.open_sprite if self.is_open else self.closed_sprite
        self.is_open = not self.is_open
        self.suffix = "(closed)" if not self.is_open else "(open)"
        self.location.area.tiles[self.y, self.x]["transparent"] = self.is_open
        self.location.area.tiles[self.y, self.x]["move_cost"] = int(self.is_open)
        self.location.area.update_fov()
