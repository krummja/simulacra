from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import Component


class Motility(Component):
    facing = (0, 0)
    facings = {
        ( 0,  0): 'static',
        ( 0,  1): 'down',
        ( 0, -1): 'up',
        (-1,  0): 'left',
        ( 1,  0): 'right',
        }

    def on_try_move(self, evt):
        success = evt.data[0]
        direction = evt.data[1]

        if success:
            self.set_facing(*direction)
            self.update_position(*direction)
            evt.handle()
        else:
            self.set_facing(*direction)
            evt.prevent()

    def set_facing(self, x, y):
        self.facing = (x, 0)
        self.update_sprite()

    def update_sprite(self):
        self.entity['SPRITE'].set_facing(self.facings[self.facing])

    def update_position(self, x, y):
        pos_x, pos_y = self.entity['POSITION'].xy
        target_x = pos_x + x
        target_y = pos_y + y
        self.entity['POSITION'].x = target_x
        self.entity['POSITION'].y = target_y
