"""ENGINE.ENTITIES.Character"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from engine.events import Actor
import engine.events.base_ai as ai

from .entity import Entity

if TYPE_CHECKING:
    from engine.events.control import Control
    from engine.areas import Location
    from engine.entities import Pronoun


class Character(Actor, Entity):
    """Character base class. Extends an Entity with Actor functionality."""

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
        self.control = ai.BasicNPC(self)
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
