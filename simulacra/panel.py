from __future__ import annotations
from typing import Dict, Tuple, TYPE_CHECKING

import tcod

from config import CONSOLE_HEIGHT, CONSOLE_WIDTH
from geometry import Rect
from util import flatten

if TYPE_CHECKING:
    from tcod.console import Console


class Panel:

    x: int = 0
    y: int = 0
    size_width: int = 0
    size_height: int = 0
    position: Tuple[str, str] = ('top', 'left')
    offset_x: int = 0
    offset_y: int = 0
    margin: int = 0
    style_fg: Tuple[int, int, int] = (255, 255, 255)
    style_bg: Tuple[int, int, int] = (0, 0, 0)
    style_framed: bool = False
    style_title: str = ''

    def __init__(self, parent: Panel = None, **config):
        self.parent: Panel = parent

        opts = flatten(config)
        for k, v in opts.items():
            setattr(self, k, v)

        if self.parent is None:
            if self.position[0] == 'top':
                self.y = 0 + self.margin
            elif self.position[0] == 'bottom':
                self.y = CONSOLE_HEIGHT - self.size_height - self.margin
            elif self.position[0] == 'center':
                self.y = (CONSOLE_HEIGHT - self.size_height) // 2

            if self.position[1] == 'left':
                self.x = 0 + self.margin
            elif self.position[1] == 'right':
                self.x = CONSOLE_WIDTH - self.size_width - self.margin
            elif self.position[1] == 'center':
                self.x = (CONSOLE_WIDTH - self.size_width) // 2

        else:
            if self.position[0] == 'top':
                self.y = self.parent.bounds.top + self.margin
            elif self.position[0] == 'bottom':
                self.y = self.parent.bounds.bottom \
                    - self.size_height - self.margin
            elif self.position[0] == 'center':
                self.y = (self.parent.bounds.bottom - (
                    self.parent.size_height // 2)) - (self.size_height // 2)

            if self.position[1] == 'left':
                self.x = self.parent.bounds.left + self.margin
            elif self.position[1] == 'right':
                self.x = self.parent.bounds.right \
                    - self.size_width - self.margin
            elif self.position[1] == 'center':
                self.x = (self.parent.bounds.right - (
                        self.parent.size_width // 2)) - (self.size_width // 2)

        self.x += self.offset_x
        self.y += self.offset_y

        self.bounds = Rect.from_edges(
            top=self.y,
            bottom=self.y + self.size_height,
            left=self.x,
            right=self.x + self.size_width
            )

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['INTERFACE'].tiles_rgb[self.bounds.indices]["ch"] = 127
        consoles['INTERFACE'].tiles_rgb[self.bounds
                                            .indices]["fg"] = self.style_bg
        consoles['INTERFACE'].tiles_rgb[self.bounds
                                            .indices]["bg"] = self.style_bg

        if self.style_framed:
            consoles['INTERFACE'].draw_frame(
                x=self.x,
                y=self.y,
                width=self.size_width,
                height=self.size_height,
                fg=self.style_fg,
                bg=self.style_bg,
                # bg_blend=tcod.BKGND_MULTIPLY
                )

        if self.style_title:
            consoles['INTERFACE'].print(
                x=self.x + 2,
                y=self.y,
                string=self.style_title,
                fg=(255, 255, 255)
                )

        consoles['INTERFACE'].blit(
            dest=consoles['ROOT'],
            dest_x=self.x,
            dest_y=self.y,
            src_x=self.x,
            src_y=self.y,
            width=self.size_width,
            height=self.size_height,
            )
