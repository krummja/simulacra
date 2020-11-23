from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING

from entity import Entity
from actor import Actor
from behaviors.base_ai import BasicNPC

if TYPE_CHECKING:
    from control import Control
    from location import Location


class Character(Entity, Actor):

    def __init__(
            self,
            uid: str,
            name: str,
            location: Location = None,
            display: Dict[str, Any] = None,
            control: Control = None
        ) -> None:
        Entity.__init__(self, location)
        self.ident = uid
        self.name = name
        self.char = display['char']
        self.color = display['color']
        self.bg = display['bg']
        self.control = BasicNPC(self)
        Actor.__init__(self, self, self.control)
