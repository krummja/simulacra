from __future__ import annotations
from typing import List, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.model import Model
    from engine.game_object import GameObject


class Component:
    ident: str = "<unnamed>"
    depends: List[str] = []

    def __init__(self: Component, owner: GameObject) -> None:
        self.owner = owner
