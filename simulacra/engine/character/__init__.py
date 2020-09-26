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

if TYPE_CHECKING:
    from engine.actions import Action
    from engine.location import Location


class Character(Graphic):
    """The Character class creates new instances through an Actor factory."""
    
    render_order: int = 0
    
    DEFAULT_AI: Type[Action] = BasicNPC

    def __init__(self, background, path) -> None:
        self.alive = True
        self.name = "<No Name>"
        self.background = background
        self.path = path

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