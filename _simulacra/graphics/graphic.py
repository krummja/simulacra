from __future__ import annotations
from graphics.colors import (Color)


class Graphic:
    char: int = 0
    foreground: Color = (255, 255, 255)
    background: Color = (0, 0, 0)
    render_order: int = 0

    def __lt__(self, other: Graphic) -> bool:
        return self.render_order < other.render_order