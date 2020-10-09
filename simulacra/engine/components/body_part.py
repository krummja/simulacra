from __future__ import annotations
from typing import TYPE_CHECKING

from engine.components import Component

if TYPE_CHECKING:
    from engine.game_object import GameObject


class BodyPart(dict):

    def __init__(
            self: BodyPart,
            owner: GameObject,
            ident: str,
            vital: bool=False,
        ) -> None:
        super().__init__()
        self.owner = owner

        self['ident'] = ident
        self['vital'] = vital

        self['slot0'] = None
        self['slot1'] = None

        if self['ident'].split('_')[0] == 'HAND':
            self['slot_equipped'] = None
