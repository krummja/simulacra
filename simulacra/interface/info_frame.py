from __future__ import annotations  # type: ignore
from typing import Dict, TYPE_CHECKING, Tuple

from constants import *
from interface.panel import Panel
from geometry import *

if TYPE_CHECKING:
    import tcod.console as Console


class InfoFrame(Panel):

    def __init__(
            self,
            x: int=0,
            y: int=0,
            position: Tuple[str, str]=None,
            parent: Panel=None,
            width: int=0,
            height: int=0,
            fg: Tuple[int, int, int]=(255, 255, 255),
            bg: Tuple[int, int, int]=(0, 0, 0),
        ) -> None:
        super().__init__(
            x=x,
            y=y,
            position=position,
            parent=parent,
            width=width,
            height=height,
            fg=fg,
            bg=bg
        )