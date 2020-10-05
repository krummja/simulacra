from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.model import Model
    from engine.game_object import GameObject


class Component:

    def __init__(self: Component, game_object: GameObject) -> None:
        self.game_object = game_object
