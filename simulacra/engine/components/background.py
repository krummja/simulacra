from __future__ import annotations

from engine.components import Component
from engine.game_object import GameObject


class Background(Component):

    _name: str = "untested"

    @property
    def name(self: Background) -> str:
        return self._name

    @name.setter
    def name(self: Background, value: str) -> None:
        self._name = value
