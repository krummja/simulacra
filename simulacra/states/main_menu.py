from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import tcod

from . import State


class MainMenu(State[None]):

    def __init__(self) -> None:
        super().__init__()