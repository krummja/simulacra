"""
The states package deals with the core state system of the game.

For this, I will be implementing some of the ideas used when putting together
Anathema.
"""

from __future__ import annotations

from typing import (Callable, Dict, Generic, Optional, TYPE_CHECKING,
                    Tuple, TypeVar)

import tcod.event

import config

if TYPE_CHECKING:
    from tcod.console import Console


Vec = Tuple[int, int]
T = TypeVar("T")


class StateBreak(Exception):
    """Breaks the active State loop and makes it return None."""


class SaveAndQuit(Exception):
    pass


class GameOverQuit(Exception):
    pass


class State(Generic[T], tcod.event.EventDispatch[T]):

    def __init__(self: State) -> None:
        super().__init__()
        self.COMMAND_KEYS: Dict[int, str] = {
            tcod.event.K_d: "drop",
            tcod.event.K_i: "inventory",
            tcod.event.K_g: "pickup",
            tcod.event.K_ESCAPE: "escape",
            tcod.event.K_RETURN: "confirm",
            tcod.event.K_KP_ENTER: "confirm",
            }

        self.MOVE_KEYS: Dict[int, Vec] = {
            # Arrow keys.
            tcod.event.K_LEFT: (-1, 0),
            tcod.event.K_RIGHT: (1, 0),
            tcod.event.K_UP: (0, -1),
            tcod.event.K_DOWN: (0, 1),
            tcod.event.K_HOME: (-1, -1),
            tcod.event.K_END: (-1, 1),
            tcod.event.K_PAGEUP: (1, -1),
            tcod.event.K_PAGEDOWN: (1, 1),
            tcod.event.K_PERIOD: (0, 0),
            # Numpad keys.
            tcod.event.K_KP_1: (-1, 1),
            tcod.event.K_KP_2: (0, 1),
            tcod.event.K_KP_3: (1, 1),
            tcod.event.K_KP_4: (-1, 0),
            tcod.event.K_KP_5: (0, 0),
            tcod.event.K_CLEAR: (0, 0),
            tcod.event.K_KP_6: (1, 0),
            tcod.event.K_KP_7: (-1, -1),
            tcod.event.K_KP_8: (0, -1),
            tcod.event.K_KP_9: (1, -1),
            # Vi keys.
            tcod.event.K_h: (-1, 0),
            tcod.event.K_j: (0, 1),
            tcod.event.K_k: (0, -1),
            tcod.event.K_l: (1, 0),
            tcod.event.K_y: (-1, -1),
            tcod.event.K_u: (1, -1),
            tcod.event.K_b: (-1, 1),
            tcod.event.K_n: (1, 1),
            }

    def loop(self: State[T]) -> Optional[T]:
        self.on_draw(config.CONSOLES)
        config.CONTEXT.present(config.CONSOLES['ROOT'])

        while True:
            for input_event in tcod.event.wait():
                try:
                    value = self.dispatch(input_event)
                except StateBreak:
                    return None
                if value is not None:
                    return value

    def on_draw(self: State[T], consoles: Dict[str, Console]) -> None:
        raise NotImplementedError()

    def ev_quit(self: State[T], event: tcod.event.Quit) -> Optional[T]:
        return self.cmd_quit()

    def ev_keydown(self: State[T], keycode: tcod.event.KeyDown) -> Optional[T]:
        func: Callable[[], Optional[T]]
        if keycode.sym in self.COMMAND_KEYS:
            func = getattr(self, f"cmd_{self.COMMAND_KEYS[keycode.sym]}")
            return func()
        if keycode.sym in self.MOVE_KEYS:
            return self.cmd_move(*self.MOVE_KEYS[keycode.sym])
        return None

    def cmd_confirm(self: State[T]) -> Optional[T]:
        pass

    def cmd_escape(self: State[T]) -> Optional[T]:
        raise StateBreak()

    def cmd_move(self: State[T], x: int, y: int) -> Optional[T]:
        pass

    def cmd_quit(self: State[T]) -> Optional[T]:
        raise SystemExit()
