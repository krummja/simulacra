from __future__ import annotations
from typing import Optional, Union

from ecstremity import Component


class Renderable(Component):
    name = "RENDERABLE"
    def __init__(self, codepoint: str, row: int = 0, col: int = 0) -> None:
        if isinstance(codepoint, str):
            self.char = int(codepoint, base=16) + (16 * row) + col
        else:
            self.char = codepoint + (16 * row) + col
        self.render_order: int = 0

    def __lt__(self, other: Renderable) -> bool:
        return self.render_order < other.render_order
