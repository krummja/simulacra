from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import Component

if TYPE_CHECKING:
    from simulacra.data.actions.action import Action
    from simulacra.core.game import Game


class Motility(Component):
    name = "MOTILITY"

    def on_try_move(self, evt):
        if isinstance(evt.data, bool):
            if evt.data == False:
                evt.prevent()
        else:
            position = self.entity['POSITION']
            target_x = position.x + evt.data[0]
            target_y = position.y + evt.data[1]
            self.entity['POSITION'].xy = (target_x, target_y)
            evt.handle()
