from __future__ import annotations
from typing import TYPE_CHECKING

from actor import Actor
from player_control import PlayerControl
from entity import Entity

from components.stats import Stats
from components.physics import Physics

if TYPE_CHECKING:
    from location import Location


class Player(Entity, Actor):

    uid = 'PLAYER'
    char = 228
    color = (255, 0, 255)
    bg = (0, 0, 0)

    def __init__(self, name: str, location: Location):
        Entity.__init__(self, self.uid, location)
        self._noun_text = name
        
        self.control = PlayerControl(self)
        Actor.__init__(self, self, self.control)