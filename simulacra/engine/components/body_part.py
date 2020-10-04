from __future__ import annotations
from typing import TYPE_CHECKING

from engine.components import Component

if TYPE_CHECKING:
    from engine.game_object import GameObject


class BodyPart(dict, Component):

    def __init__(
            self: BodyPart,
            game_object: GameObject,
            ident: str,
            vital: bool=False,
        ) -> None:
        Component.__init__(self, game_object)

        self['ident'] = ident
        self['vital'] = vital

        self['slot0'] = None
        self['slot1'] = None

        if self['ident'].split('_')[0] == 'HAND':
            self['slot_equipped'] = None
