from __future__ import annotations
from typing import Tuple, Union

from ecstremity import Component


class Renderable(Component):
    name = "RENDERABLE"
    def __init__(
            self,
            char: Union[str, int]
        ) -> None:
        if isinstance(char, str):
            self.char = ord(char)
        else:
            self.char = char
        self.render_order: int = 0

    def __lt__(self, other: Renderable) -> bool:
        return self.render_order < other.render_order
