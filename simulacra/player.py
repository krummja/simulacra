from __future__ import annotations
from typing import TYPE_CHECKING

from actor import Actor
from control import PlayerControl
from entity import Entity

from components.attributes import Attributes
from components.physics import Physics

if TYPE_CHECKING:
    from location import Location


class Player(Entity, Actor):

    ident = 'PLAYER'
    char = ord("@")
    color = (255, 0, 255)
    bg = (0, 0, 0)

    def __init__(self, location: Location):
        Entity.__init__(self, location)

        self.control = PlayerControl(self)
        Actor.__init__(self, self, self.control)

        self.components.add(Physics(self))
        self.components.add(Attributes(self))
