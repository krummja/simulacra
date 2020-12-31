"""ENGINE.ENTITIES.Player"""
from __future__ import annotations

from typing import TYPE_CHECKING

from engine.events.actor import Actor
from engine.events.player_control import PlayerControl
from engine.entities import Pronoun

from .entity import Entity

if TYPE_CHECKING:
    from engine.areas import Location


class Player(Entity, Actor):
    """Player."""

    uid = 'PLAYER'
    char = ord("@")
    color = (200, 100, 130)
    bg = (0, 0, 0)

    def __init__(self, name: str, location: Location):
        Entity.__init__(self, self.uid, location)
        self._name = name
        self._noun_text = 'you'

        self.control = PlayerControl(self)
        Actor.__init__(self, owner=self, control=self.control)

    @property
    def pronoun(self) -> Pronoun:
        return Pronoun.you

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name
