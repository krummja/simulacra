from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING

from entity import Entity
from actor import Actor
from behaviors.base_ai import BasicNPC

if TYPE_CHECKING:
    from control import Control
    from location import Location


class Character(Actor, Entity):

    def __init__(
            self,
            uid: str,
            name: str,
            location: Location = None,
            display: Dict[str, Any] = None,
        ) -> None:
        """Either a Player Character or an NPC. Has a Control instance.

        Args:
            uid (str): Backend identifier, for UI & Factory systems.
            name (str): Frontend identifier, for in-game reference.
            location (Location, optional): Where it's at. Defaults to None.
            display (Dict[str, Any], optional): Display props. Defaults to None.
        """        
        Entity.__init__(self, location)
        self.uid = uid
        self.noun_text = name
        self.char = display['char']
        self.color = display['color']
        self.bg = display['bg']
        self.control = BasicNPC(self)
        Actor.__init__(self, self, self.control)
