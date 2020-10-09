from __future__ import annotations
from typing import List, Type, TYPE_CHECKING

from engine.components import Component

if TYPE_CHECKING:
    from engine.model import Model
    from engine.game_object import GameObject


class Physics(Component):
    ident: str = "<unnamed>"

    def __init__(
            self: Component,
            owner: GameObject,
            weight: int
        ) -> None:
        super().__init__(owner)
        self.weight = weight

    @property
    def movable(self: Physics) -> bool:
        if self.weight == -1:
            return False
        else:
            return True
