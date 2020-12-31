from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING, Tuple, Optional

import tcod
from config import *

from interface.views.view import View
from interface.elements.base_element import BaseElement, ElementConfig


if TYPE_CHECKING:
    from tcod.console import Console
    from engine.states.state import State
    from engine.entities.entity import Entity


class GaugeElement(BaseElement):

    def __init__(
            self,
            config: ElementConfig,
            hue: Tuple[int, int, int],
            data: Tuple[float, float]
        ) -> None:
        super().__init__(config)
        self.hue = hue
        self._data = data

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].print(
            self.x + 8, self.y,
            str(int(self._data[0])).center(self.width)[:self.width],
            fg=(255, 255, 255))

        current_value = self._data[0] / self._data[1]
        bar_bg = consoles['ROOT'].tiles_rgb.T["bg"][
            self.x + 8:self.x + 8 + self.width, self.y]
        bg_hue = (self.hue[0] // 2, self.hue[1] // 2, self.hue[2] // 2)
        bar_bg[...] = bg_hue

        fill_width = max(0, min(self.width, int(current_value * self.width)))
        bar_bg[:fill_width] = self.hue
