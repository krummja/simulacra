from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.actions import *
from engine.actions import common
from engine.items import Item
from engine.graphic import Graphic
from content.tiles import font_map
from engine.hues import COLOR

if TYPE_CHECKING:
    from engine.actor import Actor


class Corpse(Item):

    char = ord("%")
    color = (127, 0, 0)
    render_order = 2

    def __init__(self, actor: Actor) -> None:
        super().__init__()
        self.name = f"{actor.character.name} Corpse"


class Door(Item):

    char = font_map['door_01']
    color = COLOR['chocolate']
    render_order=1

    def __init__(self):
        super().__init__()
        self.is_interactable = True
        self.is_blocked = False
        self.is_closed = True
        self.is_locked = False

    def plan_activate(self, action: ActionWithItem) -> ActionWithItem:
        if self.is_locked: 
            raise Impossible("The door is locked.")
        if self.is_closed:
            return common.Open(action.actor, self)
        return action

    def open(self) -> None:
        if self.is_closed:
            print("Door opens")
            self.char = font_map['wood_01']
            self.color = COLOR['dark chocolate']
            self.is_interactable = False
            self.is_closed = False

    def close(self) -> None:
        if self.is_open:
            print("Door closes")
            self.char = font_map['door_01']
            self.color = COLOR['chocolate']
            self.is_interactable = True
            self.is_closed = True