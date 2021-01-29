from __future__ import annotations
from typing import TYPE_CHECKING

from .system import System
from simulacra.core.options import *
from simulacra.utils.render_utils import *

if TYPE_CHECKING:
    from simulacra.core.game import Game


class AnimationSystem(System):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self._query = self.ecs.create_query(
            all_of=[  'RENDERABLE',
                      'POSITION',
                      'SPRITE'      ],
            none_of=[ 'INVISIBLE'   ])

    def play(self, dt) -> None:
        for entity in self._query.result:
            sprite = entity['SPRITE']

