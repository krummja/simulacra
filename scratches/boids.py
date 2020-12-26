from __future__ import annotations

from p5 import setup, draw, size, background, run


class Boid:
    def __init__(self, x, y, height, width):
        self.position = Vector(x, y)