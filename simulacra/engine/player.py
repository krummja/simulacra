from __future__ import annotations
from typing import Optional, Tuple, Type, TYPE_CHECKING

from engine.actor import Actor
from engine.game_object import GameObject
from engine.components.body_part import BodyPart
from engine.components.attributes import Attributes
from engine.components.inventory import Inventory


if TYPE_CHECKING:
    from engine.actions.behaviors import Behavior
    from engine.location import Location


class Player(GameObject):

    def __init__(
            self: Player,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
        ) -> None:
        super().__init__(char, color, bg, noun_text, location)

        self.components['attributes'] = Attributes(self)
        self.components['inventory'] = Inventory(self)
        self.components['equipment'] = Inventory(self)

        self.components['HEAD'] = BodyPart(self, 'HEAD', True),
        self.components['TORSO'] = BodyPart(self, 'TORSO', True),
        self.components['ARM_LEFT'] = BodyPart(self, 'ARM_LEFT', False),
        self.components['HAND_LEFT'] = BodyPart(self, 'HAND_LEFT', False),
        self.components['ARM_RIGHT'] = BodyPart(self, 'ARM_RIGHT', False),
        self.components['HAND_RIGHT'] = BodyPart(self, 'HAND_RIGHT', False),
        self.components['LEG_LEFT'] = BodyPart(self, 'LEG_LEFT', False),
        self.components['LEG_RIGHT'] = BodyPart(self, 'LEG_RIGHT', False)

    @classmethod
    def spawn(
            cls,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            behavior: Optional[Type[Behavior]]
        ) -> Actor:
        self = cls(char, color, bg, noun_text, location)
        return Actor(location, self, behavior)
