from __future__ import annotations
from typing import Generator

from ecstremity import Component


class Sprite(Component):

    def __init__(self, sheet: int = 0xE500, row: int = 0) -> None:
        self.sheet: int = sheet
        self.row: int = 16 * row
        self.codepoint: int = sheet + self.row

        self.facing = {
            'left' : 0,
            'right'  : 1,
            }

    def set_facing(self, key: str) -> None:
        if key == 'left' or key == 'right':
            self.entity['RENDERABLE'].char = self.codepoint + self.facing[key]
