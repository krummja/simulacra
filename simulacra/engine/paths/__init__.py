from __future__ import annotations  # type: ignore
from typing import Optional, Type, TYPE_CHECKING


from engine.actor import Actor
from engine.graphic import *

if TYPE_CHECKING:
    from engine.actions import Action
    from engine.location import Location


class Fighter(Graphic):

    render_order: int = 0
    hp: int = 0
    power: int = 0
    defense: int = 0

    def __init__(self) -> None:
        self.alive = True
        self.max_hp = self.hp
    
    @classmethod
    def spawn(cls, location: Location, ai_cls: Optional[Type[Action]]=None) -> Actor: 
        self = cls()
        return Actor(location, self, ai_cls)