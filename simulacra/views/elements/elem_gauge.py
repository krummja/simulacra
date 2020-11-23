from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Dict, Tuple

from panel import Panel

if TYPE_CHECKING:
    from tcod.console import Console


class ElemGauge(Panel):

    name: str
    text: str
    fullness: float
    fg: Tuple[int, int, int]
    bg: Tuple[int, int, int]
    text_fg: Tuple[int, int, int]

    def __init__(
            self,
            parent: Panel,
            position: Tuple[str, str],
            margin: int,
            offset_x: int,
            offset_y: int,
            width: int,
            name: str,
            text: str,
            fullness: float,
            fg: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            text_fg: Tuple[int, int, int],
        ) -> None:
        super().__init__(**{
            'parent': parent,
            'position': position,
            'margin': margin,
            'offset': {'x': offset_x,
                       'y': offset_y},
            'size': {'width': width,
                     'height': 1}
            })
        self.name = name
        self.text = text
        self.fullness = fullness
        self.fg = fg
        self.bg = bg
        self.text_fg = text_fg

    def draw(self, consoles: Dict[str, Console]) -> None:
        self.on_draw(consoles)
        consoles['ROOT'].print(
            self.x - 6, self.y,
            self.name + ": ",
            fg=(255, 255, 255)
            )

        consoles['ROOT'].print(
            self.x, self.y,
            self.text.center(self.size_width)[:self.size_width],
            fg=self.text_fg
            )

        bar_bg = consoles['ROOT'].tiles_rgb.T["bg"][self.x:self.x + self.size_width, self.y]
        bar_bg[...] = self.bg

        fill_width = max(0, min(self.size_width, int(self.fullness * self.size_width)))
        bar_bg[:fill_width] = self.fg
