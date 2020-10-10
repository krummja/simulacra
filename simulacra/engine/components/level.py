from __future__ import annotations
from typing import List, TYPE_CHECKING

from engine.components import Component


class Level(Component):
    _current_level: int = 1

    @property
    def current_level(self: Level) -> int:
        return self._current_level

    @current_level.setter
    def current_level(self: Level, value: int) -> None:
        self._current_level = value
