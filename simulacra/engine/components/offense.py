from __future__ import annotations
from typing import List, TYPE_CHECKING

from engine.components import Component

if TYPE_CHECKING:
    from engine.game_object import GameObject
    from engine.items import Item
    from engine.actions import Action


class Offense(Component):

    def __init__(self: Offense, game_object: GameObject) -> None:
        super().__init__(game_object)

    def plan_attack(self: Offense, action: Action) -> Action:
        return action

    def attack(self: Offense, target: GameObject) -> None:
        pass
