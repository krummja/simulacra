from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING

from entity import Entity
from actor import Actor
from behaviors.base_ai import BasicNPC

if TYPE_CHECKING:
    from control import Control
    from location import Location
    from noun import Pronoun


class Character(Actor, Entity):

    def __init__(
            self,
            uid: str,
            name: str,
            location: Location = None,
            display: Dict[str, Any] = None,
            gender: str = None
        ) -> None:     
        Entity.__init__(self, uid, location)
        self._noun_text = name
        self.char = display['char']
        self.color = display['color']
        self.bg = display['bg']
        self.gender = gender
        self.control = BasicNPC(self)
        Actor.__init__(self, self, self.control)

    @property
    def name(self) -> str:
        return self._noun_text
    
    @property
    def pronoun(self) -> Pronoun:
        if self.gender is not None:
            if self.gender == "masc":
                return Pronoun.he
            elif self.gender == "fem":
                return Pronoun.she
            else:
                return Pronoun.they
        else:
            return Pronoun.it
