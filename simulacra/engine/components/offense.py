from __future__ import annotations
from typing import List, TYPE_CHECKING

from engine.components import Component

if TYPE_CHECKING:
    from engine.game_object import GameObject
    from engine.items import Item
    from engine.actions import Action


class Offense(Component):

    def __init__(self: Offense, owner: GameObject) -> None:
        super().__init__(owner)

    @property
    def attack(self: Offense) -> int:
        might = self.owner.components['ATTRIBUTES']['might']
        finesse = self.owner.components['ATTRIBUTES']['finesse']
        intellect = self.owner.components['ATTRIBUTES']['intellect']

        attack = might
        return attack

    def plan_attack(self: Offense, action: Action) -> Action:
        return action
