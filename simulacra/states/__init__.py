from __future__ import annotations  # type: ignore
from typing import Callable, Generic, Optional, TypeVar, TYPE_CHECKING

import tcod
import tcod.console as Console
import tcod.event

from simulacra.consoles import *
from simulacra.constants import *

from .main_menu import MainMenu

T = TypeVar("T")


class StateBreak(Exception):
    """Breaks out of the active State.loop and makes it return None."""


class State(Generic[T], tcod.event.EventDispatch[T]):

    def loop(self) -> Optional[T]:
        """Run a state-based game loop."""

        while True:
            pass

    def on_draw(self, console: Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[T]:
        pass

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        pass

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_escape(self) -> Optional[T]:
        raise StateBreak()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_quit(self) -> Optional[T]:
        raise SystemExit()