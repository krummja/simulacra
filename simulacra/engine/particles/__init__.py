from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import random
import time
import tcod

# https://code.harrywykman.com/implementing-a-simple-particle-system-in-python-using-libtcod.html


class Particle:

    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.moves = 0