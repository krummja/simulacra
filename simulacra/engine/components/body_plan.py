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

        self.instance_legs()
        self.instance_arms()

    def instance_legs(self: BodyPlan) -> None:
        pass

    def instance_arms(self: BodyPlan) -> None:
        if self.arms == 2:
            if self.symmetric:
                for side in self.sides:
                    self['ARMS'] = BodyPart(
                        self.game_object,
                        f"ARM_{side}",
                        False
                        )
                    self['HANDS'] = BodyPart(
                        self.game_object,
                        f"HAND_{side}",
                        False
                        )

        if self.arms == 4:
            if self.symmetric:
                for position in self.positions:
                    for side in self.sides:
                        self['ARMS'] = BodyPart(
                            self.game_object,
                            f"ARM_{position}_{side}",
                            False
                            )
                        self['HANDS'] = BodyPart(
                            self.game_object,
                            f"HAND_{position}_{side}",
                            False
                            )
