from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import Component


class Motility(Component):
    name = "MOTILITY"
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
            self.update_position(*self.set_facing(*direction))
            evt.handle()
        else:
            self.set_facing(*direction)
            evt.prevent()

    def set_facing(self, x, y):
        position = self.entity['POSITION']

        if x == self.facing[0] and y == self.facing[1]:
            target_x = position.x + x
            target_y = position.y + y
            return target_x, target_y

        else:
            target_x = position.x
            target_y = position.y
            self.facing = (x, y)
            self.update_sprite()
            return target_x, target_y

    def update_sprite(self):
        self.entity['SPRITE'].set_facing(self.facings[self.facing])

    def update_position(self, x, y):
        self.entity['POSITION'].xy = x, y
