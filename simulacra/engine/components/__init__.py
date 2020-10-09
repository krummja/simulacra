from __future__ import annotations
from typing import List, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.model import Model
    from engine.game_object import GameObject


class Component:
    ident: str = "<unnamed>"
    _option: str = ""

    def __init__(self: Component, owner: GameObject) -> None:
        self.owner = owner

    @property
    def option(self: Component) -> str:
        return self._option

    @option.setter
    def option(self: Component, value: str) -> None:
        self._option = value
