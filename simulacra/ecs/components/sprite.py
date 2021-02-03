from __future__ import annotations
from typing import Generator

from ecstremity import Component


class Sprite(Component):
    name = "SPRITE"

    def __init__(self, sheet: int = 0xE500, row: int = 0) -> None:
        self.sheet: int = sheet
        self.row: int = 16 * row
        self.codepoint: int = sheet + row

        self.facing = {
            'left'  : 0,
            'right' : 1,
            }

        self.animations = {
            'walk down'  : [ 4, 0, 5  ],
            'walk up'    : [ 6, 1, 7  ],
            'walk left'  : [ 8, 2, 8  ],
            'walk right' : [ 9, 3, 10 ],
            }

    def set_facing(self, key: str) -> None:
        if key == 'left' or key == 'right':
            self.entity['RENDERABLE'].char = self.codepoint + self.facing[key]

    def get_animation(self, key: str) -> Generator[int, None, None]:
        animation_list = self.animations[key]
        for value in animation_list:
            yield self.codepoint + value
