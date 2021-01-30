from __future__ import annotations
from typing import TYPE_CHECKING

from simulacra.core.options import *

from .element import Element, ElementConfig

if TYPE_CHECKING:
    from .ui_manager import UIManager


class Surface(Element):

    def __init__(self, manager: UIManager, **kwargs) -> None:
        super().__init__(manager, **kwargs)
        self._sprites = {
            'top_left'     : 0xEF00 + (16*0),
            'top_right'    : 0xEF02 + (16*0),
            'bottom_left'  : 0xEF00 + (16*2),
            'bottom_right' : 0xEF02 + (16*2),
            'left'         : 0xEF00 + (16*1),
            'top'          : 0xEF01 + (16*0),
            'right'        : 0xEF02 + (16*1),
            'bottom'       : 0xEF01 + (16*2),
            'center'       : 0xEF01 + (16*1),
            }

    def draw_content(self, dt) -> None:
        self.fill_container()
        self.console.color(0xFF000000)
        self.console.layer(6)
        self.console.puts(self.content.left, self.content.top, "Test")

    def fill_container(self) -> None:
        top_left = self.x, self.y
        top_right = self.x + self.width - 4, self.y
        bottom_left = self.x, self.y + self.height - 2
        bottom_right = self.x + self.width - 4, self.y + self.height - 2

        # Position the four corner sprites.
        self.console.put(*top_left, c=self._sprites['top_left'])
        self.console.put(*top_right, c=self._sprites['top_right'])
        self.console.put(*bottom_left, c=self._sprites['bottom_left'])
        self.console.put(*bottom_right, c=self._sprites['bottom_right'])

        # Draw the frame.
        horizontal = range(self.x + 4, self.x + self.width - 7, 4)
        for x in horizontal:
            self.console.put(x, self.y, c=self._sprites['top'])
            self.console.put(x, self.height - 2, c=self._sprites['bottom'])

        vertical = range(self.y + 2, self.y + self.height - 3, 2)
        for y in vertical:
            self.console.put(self.x, y, c=self._sprites['left'])
            self.console.put(self.x + self.width - 4, y, c=self._sprites['right'])

        # Fill the inner area.
        for x in range(self.x + 2, self.x + self.width - 2, 4):
            for y in range(self.y + 2, self.y + self.height - 3, 2):
                self.console.put(x, y, c=self._sprites['center'])
