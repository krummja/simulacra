from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from engine.components import Component

if TYPE_CHECKING:
    from engine.components.body_part import BodyPart
    from engine.game_object import GameObject


class BodyPlan(dict, Component):

    def __init__(
            self: BodyPlan,
            game_object: GameObject,
            legs: int,
            arms: int,
            heads: int,
            tails: int,
            eyes: int,
            vertebrate: bool,
            symmetric: bool,
            neuraxis: str
            ) -> None:
        super().__init__(game_object)
        self.legs = legs
        self.arms = arms
        self.heads = heads
        self.tails = tails
        self.eyes = eyes
        self.vertebrate = vertebrate
        self.symmetric = symmetric
        self.neuraxis = neuraxis

        self.sides = ['LEFT', 'RIGHT']
        self.positions = ['TOP', 'BOTTOM', 'FRONT', 'BACK']


class Body(dict, Component):
    def __init__(self: Body, owner: GameObject) -> None:
        dict.__init__(self)
        Component.__init__(self, owner)

    def add_part(self: Body, part: BodyPart) -> None:
        self[part['ident']] = part

    def get_part(self: Body, part: str) -> BodyPart:
        return self[part]
