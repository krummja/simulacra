from __future__ import annotations  # type: ignore
from typing import Optional, Type, TYPE_CHECKING

from engine.actor import Actor
from engine.actions.ai import *
from engine.graphic import *
from engine.character.attribute import Attribute

if TYPE_CHECKING:
    from engine.actions import Action
    from engine.location import Location


class Object(Graphic):

    render_order: int = 0

    def __init__(self) -> None:
        self.name: str = ""
        self.interactable_flag: bool = True
    
    @property
    def is_interactable(self) -> bool:
        return self.interactable_flag

    @is_interactable.setter
    def is_interactable(self, value: bool) -> None:
        self.interactable_flag = value

    @classmethod
    def spawn(
            cls,
            location: Location,
            ai_cls: Optional[Type[Action]]=None
        ) -> Actor:
        self = cls()
        return Actor(location, self, ai_cls)