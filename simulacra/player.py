from __future__ import annotations

from typing import TYPE_CHECKING

from actor import Actor
from entity import Entity
from noun import Pronoun
from player_control import PlayerControl

if TYPE_CHECKING:
    from location import Location


class Player(Entity, Actor):

    uid = 'PLAYER'
    char = ord("@")
    color = (200, 100, 130)
    bg = (0, 0, 0)

    def __init__(self, name: str, location: Location):
        Entity.__init__(self, self.uid, location)
        self._name = name
        self._noun_text = 'you'

        self.control = PlayerControl(self)
        Actor.__init__(self, self, self.control)

    @property
    def pronoun(self) -> Pronoun:
        return Pronoun.you

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name
