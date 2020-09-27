from __future__ import annotations  # type: ignore
from typing import Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    import tcod.console as Console
    from engine.model import Model


class Gauge:

    def __init__(
            self, 
            x: int, 
            y: int,
            width: int,
            text: str,
            fullness: float,
            fg: Tuple[int, int, int],
            bg: Tuple[int, int, int],
        ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.text = text
        self.fullness = fullness
        self.fg = fg
        self.bg = bg

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].print(
            self.x, 
            self.y, 
            self.text.center(self.width)[:self.width], 
            fg=(255, 255, 255)
        )

        bar_bg = consoles['ROOT'].tiles_rgb.T["bg"][
            self.x : self.x + self.width, self.y
        ]
        bar_bg[...] = self.bg
        fill_width = max(0, min(self.width, int(self.fullness * self.width)))
        bar_bg[:fill_width] = self.fg
        