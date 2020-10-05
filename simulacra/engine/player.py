from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from engine.components.actor import Actor
from engine.actions.behaviors.player_control import PlayerControl
from engine.game_object import GameObject
from engine.components.body_part import BodyPart
from engine.components.attributes import Attributes
from engine.components.inventory import Inventory


if TYPE_CHECKING:
    from engine.location import Location


class Player(GameObject):

    def __init__(
            self: Player,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location
        ) -> None:
        super().__init__(char, color, bg, noun_text)
        self._location = location

        self.components['ACTOR'] = Actor(self, PlayerControl)

        self.components['ATTRIBUTES'] = Attributes(self)
        self.components['INVENTORY'] = Inventory(self)
        self.components['EQUIPMENT'] = Inventory(self)

        self.components['HEAD'] = BodyPart(self, 'HEAD', True),
        self.components['TORSO'] = BodyPart(self, 'TORSO', True),
        self.components['ARM_LEFT'] = BodyPart(self, 'ARM_LEFT', False),
        self.components['HAND_LEFT'] = BodyPart(self, 'HAND_LEFT', False),
        self.components['ARM_RIGHT'] = BodyPart(self, 'ARM_RIGHT', False),
        self.components['HAND_RIGHT'] = BodyPart(self, 'HAND_RIGHT', False),
        self.components['LEG_LEFT'] = BodyPart(self, 'LEG_LEFT', False),
        self.components['LEG_RIGHT'] = BodyPart(self, 'LEG_RIGHT', False)

    @property
    def location(self: Player) -> Location:
        return self._location

    @location.setter
    def location(self: Player, value: Location) -> None:
        self._location = value

    def is_player(self: Actor) -> bool:
        return self.location.area.player is self

    @classmethod
    def spawn(
            cls,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
        ) -> Player:
        self = cls(char, color, bg, noun_text, location)
        return self
