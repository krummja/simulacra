from __future__ import annotations  # type: ignore
from typing import Tuple, TYPE_CHECKING

from engine.objects import Object
from engine.actions import *
from engine.actions import common
from engine.items import Item
from engine.graphic import Graphic
from content.tiles import font_map
from engine.hues import COLOR

if TYPE_CHECKING:
    from engine.actor import Actor


class Door(Object):

    def __init__(self) -> None:
        super().__init__()
        self.is_blocked = False
        self.is_closed = True
        self.is_locked = False

    def plan_activate(self, action: ActionWithItem) -> ActionWithItem:
        pass

    def open(self) -> None:
        pass

    def close(self) -> None:
        pass


class WoodenDoor(Door):

    def __init__(self, char, color, background_tile) -> None:
        self._char: int = char
        self._color = color

    @property
    def char(self) -> int:
        return self._char

    @char.setter
    def char(self, value: int) -> None:
        self._char = value

    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color
    
    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        self._color = value