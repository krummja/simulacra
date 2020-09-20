from __future__ import annotations  # type: ignore
from typing import Optional, TYPE_CHECKING

from constants import *

if TYPE_CHECKING:
    import tcod.console as Console


class ScreenPoints:

    def __init__(self, console: Console) -> None:
        self.console = console

    @property
    def top_left(self):
        return (0, 0)



        