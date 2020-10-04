from __future__ import annotations
from typing import TYPE_CHECKING

from engine.components import Component
from engine.attribute import Attribute

if TYPE_CHECKING:
    from engine.game_object import GameObject


class Attributes(dict, Component):

    def __init__(self: Attributes, game_object: GameObject) -> None:
        Component.__init__(self, game_object)

        self['health'] = Attribute(game_object, 'health', 100)
        self['energy'] = Attribute(game_object, 'energy', 100)
        self['might'] = Attribute(game_object, 'might', 0)
        self['resilience'] = Attribute(game_object, 'resilience', 0)
        self['intellect'] = Attribute(game_object, 'intellect', 0)
        self['finesse'] = Attribute(game_object, 'finesse', 0)
