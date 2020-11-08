from __future__ import annotations
from typing import Dict, Optional, Tuple, TYPE_CHECKING

from config import *
from geometry import *

if TYPE_CHECKING:
    from tcod.console import Console


class Panel:

    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    def __init__(self, parent: Panel=None, **config):
        self.parent: Panel = parent

        for option in config:
            if option == 'size':
                self.width = config['size']['width']
                self.height = config['size']['height']

            if option == 'margin':
                self.margin = config['margin']
            else:
                self.margin = 0

            if option == 'position':
                if self.parent is None:
                    if config['position'][0] == 'top':
                        self.y = 0 + self.margin
                    elif config['position'][0] == 'bottom':
                        self.y = CONSOLE_HEIGHT - self.height - self.margin
                    elif config['position'][0] == 'center':
                        self.y = (CONSOLE_HEIGHT - self.height) // 2

                    if config['position'][1] == 'left':
                        self.x = 0 + self.margin
                    elif config['position'][1] == 'right':
                        self.x = CONSOLE_WIDTH - self.width - self.margin
                    elif config['position'][1] == 'center':
                        self.x = (CONSOLE_WIDTH - self.width) // 2

                else:
                    if config['position'][0] == 'top':
                        self.y = self.parent.bounds.top + self.margin
                    elif config['position'][0] == 'bottom':
                        self.y = self.parent.bounds.bottom - self.height - self.margin
                    elif config['position'][0] == 'center':
                        self.y = (self.parent.bounds.bottom - (
                                self.parent.height // 2)) - (self.height // 2)

                    if config['position'][1] == 'left':
                        self.x = self.parent.bounds.left + self.margin
                    elif config['position'][1] == 'right':
                        self.x = self.parent.bounds.right - self.width - self.margin
                    elif config['position'][1] == 'center':
                        self.x = (self.parent.bounds.right - (
                                self.parent.width // 2)) - (self.width // 2)

            if option == 'offset':
                self.x += config['offset']['x']
                self.y += config['offset']['y']

            if option == 'style':
                for style_opt in config['style']:
                    if style_opt == 'fg':
                        self.fg = config['style']['fg']
                    if style_opt == 'bg':
                        self.bg = config['style']['bg']
                    if style_opt == 'framed':
                        self.framed = config['style']['framed']
                    if style_opt == 'title':
                        self.title = config['style']['title']
            else:
                self.fg = (255, 255, 255)
                self.bg = (0, 0, 0)
                self.framed = False
                self.title = None

            self.bounds = Rect.from_edges(
                top=self.y,
                bottom=self.y + self.height,
                left=self.x,
                right=self.x + self.width
                )

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['INTERFACE'].tiles_rgb[self.bounds.indices]["ch"] = 127
        consoles['INTERFACE'].tiles_rgb[self.bounds.indices]["fg"] = self.bg
        consoles['INTERFACE'].tiles_rgb[self.bounds.indices]["bg"] = self.bg

        if self.framed:
            consoles['INTERFACE'].draw_frame(
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                fg=self.fg,
                bg=self.bg
                )

        if self.title:
            consoles['INTERFACE'].print(
                x=self.x + 2,
                y=self.y,
                string=self.title
                )

        consoles['INTERFACE'].blit(
            dest=consoles['ROOT'],
            dest_x=self.x,
            dest_y=self.y,
            src_x=self.x,
            src_y=self.y,
            width=self.width,
            height=self.height,
            )
