from __future__ import annotations
from typing import TYPE_CHECKING

from engine.components.actor import Actor
from engine.actions.behaviors.base_ai import BasicNPC
from engine.game_object import GameObject
from engine.components.body_part import BodyPart
from engine.components.attributes import Attributes
from engine.components.inventory import Inventory
from engine.components.equipment import Equipment
from engine.components.body_plan import Body
from engine.components.background import Background
from engine.components.level import Level

if TYPE_CHECKING:
    from engine.location import Location


class NPC(GameObject):
    char = ord("N")
    color = (0, 255, 255)
    bg = (0, 0, 0)

    def __init__(self: NPC, location: Location) -> None:
        super().__init__(location)

        self.components['BODY'] = Body(self)
        self.components['BODY'].add_part(BodyPart(self, 'HEAD', True))
        self.components['BODY'].add_part(BodyPart(self, 'TORSO', True))
        self.components['BODY'].add_part(BodyPart(self, 'ARM_LEFT', False))
        self.components['BODY'].add_part(BodyPart(self, 'HAND_LEFT', False))
        self.components['BODY'].add_part(BodyPart(self, 'ARM_RIGHT', False))
        self.components['BODY'].add_part(BodyPart(self, 'HAND_RIGHT', False))
        self.components['BODY'].add_part(BodyPart(self, 'LEG_LEFT', False))
        self.components['BODY'].add_part(BodyPart(self, 'LEG_RIGHT', False))

        self.components['ACTOR'] = Actor(self, BasicNPC)

        self.components['ATTRIBUTES'] = Attributes(self)
        self.components['INVENTORY'] = Inventory(self)
        self.components['EQUIPMENT'] = Equipment(self)

        self.components['LEVEL'] = Level(self)
        self.components['BACKGROUND'] = Background(self)

    @classmethod
    def spawn(cls, location: Location) -> NPC:
        self = cls(location)
        return self
