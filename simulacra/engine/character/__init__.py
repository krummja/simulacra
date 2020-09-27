"""A Character is a concrete Actor supplied with an AI and a set of definitional
components. For a Player Character, this might be a Path component and a
Background component, which together make up the distinct identity of that
player's character in the game world.
"""

from __future__ import annotations  # type: ignore
from typing import Optional, Type, TYPE_CHECKING

from engine.actor import Actor
from engine.actions.ai import *
from engine.graphic import *
from engine.character.attribute import Attribute

if TYPE_CHECKING:
    from engine.actions import Action
    from engine.location import Location


class Character(Graphic):
    """The Character class creates new instances through an Actor factory."""
    
    render_order: int = 0
    
    DEFAULT_AI: Type[Action] = BasicNPC

    def __init__(self, background, path) -> None:
        self.alive = True
        self.name = "TEST CHARACTER"
        self.background = background
        self.path = path
        self.combat_flag = False
        self._attributes: Dict[str, Attribute] = {
            'health': Attribute(self, 'health', 100),
            'energy': Attribute(self, 'energy', 100),
            'might': Attribute(self, 'might', 10),
            'resilience': Attribute(self, 'resilience', 4),
            'intellect': Attribute(self, 'intellect', 8),
            'finesse': Attribute(self, 'finesse', 6),
        }

    @property
    def is_combatant(self) -> bool:
        return self.combat_flag

    @is_combatant.setter
    def is_combatant(self, value: bool) -> None:
        self.combat_flag = value

    @property
    def attributes(self) -> Dict[str, Attribute]:
        return self._attributes

    def add_attribute(self, name: str, value: int) -> None:
        self._attributes[name] = Attribute(self, name, value)

    @classmethod
    def spawn(
            cls, 
            location: Location, 
            ai_cls: Optional[Type[Action]]=None
        ) -> Actor:
        background = None
        path = None
        self = cls(background, path)
        return Actor(location, self, ai_cls or cls.DEFAULT_AI)