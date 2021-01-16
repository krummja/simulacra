"""ENGINE.STATES.State"""
from __future__ import annotations

from typing import (TYPE_CHECKING, Callable, Dict, Generic, Optional, Tuple,
                    TypeVar)

import tcod

import config

if TYPE_CHECKING:
    from tcod.console import Console

    from engine.model import Model
    from engine.storage import Storage
    from interface import View

T = TypeVar("T")


class GameOverQuit(Exception):
    pass


class SaveAndQuit(Exception):
    pass


class EffectsBreak(Exception):
    pass


class StateBreak(Exception):
    """Breaks the active State loop and makes it return None."""


class State(Generic[T], tcod.event.EventDispatch[T]):
    """Component of the Controller representing the active game state.

    The core function of State is to provide a context for mapping client
    inputs into mutations on a View. Usually this will be the StageView,
    with mutations corresponding to Action instances.

    The Model property contains all of a particular session's game data.
    It is the central representation of all of the game content.
    """

    _COMMAND_KEYS: Dict[int, str] = {
        tcod.event.K_e: "equipment",
        tcod.event.K_i: "inventory",
        tcod.event.K_g: "pickup",
        tcod.event.K_ESCAPE: "escape",
        tcod.event.K_RETURN: "confirm",
        tcod.event.K_KP_ENTER: "confirm",
        tcod.event.K_l: "examine",
        }

    _MOVE_KEYS: Dict[int, Tuple[int, int]] = {
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
        }

    _DEBUG_KEYS: Dict[int, Tuple[int, str]] = {
        tcod.event.K_F1: 'debug_1',
        tcod.event.K_F2: 'debug_2',
        tcod.event.K_F3: 'debug_3',
        tcod.event.K_F4: 'debug_4'
    }

    def __init__(self) -> None:
        super().__init__()

        self._model: Optional[Model] = None
        self._storage: Optional[Storage] = None
        self._view: Optional[View] = None
        self.suspend = False

    @property
    def COMMAND_KEYS(self: State) -> Dict[int, str]:
        return self._COMMAND_KEYS

    @property
    def MOVE_KEYS(self: State) -> Dict[int, Tuple[int, int]]:
        return self._MOVE_KEYS

    @property
    def model(self) -> Optional[Model]:
        return self._model

    @property
    def storage(self) -> Optional[Storage]:
        return self._storage

    @property
    def view(self) -> Optional[View]:
        return self._view

    def loop(self) -> Optional[T]:
        while True:
            self.on_draw(config.CONSOLES)
            config.CONTEXT.present(config.CONSOLES['ROOT'])

            all_key_events = list(tcod.event.get())
            key_events = [e for e in all_key_events if e.type == 'KEYDOWN']

            if len(key_events) > 0:
                event = key_events.pop()
                try:
                    value: Optional[T] = self.dispatch(event)
                except StateBreak:
                    return None
                if value is not None:
                    if not self.suspend:
                        return value

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        self._view.draw(consoles)

    def ev_quit(self, event: tcod.event.Quit) -> Optional[T]:
        return self.cmd_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        """Checks an event against a specified input dict and returns a
        cmd_* method where defined.
        """
        func: Callable[[], Optional[T]]
        if event.sym in self.COMMAND_KEYS:
            func = getattr(self, f"cmd_{self.COMMAND_KEYS[event.sym]}")
            return func()
        if event.sym in self.MOVE_KEYS:
            return self.cmd_move(*self.MOVE_KEYS[event.sym])
        if event.sym  in self._DEBUG_KEYS:
            func = getattr(self, f"cmd_{self._DEBUG_KEYS[event.sym]}")
            return func()
        return None

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_escape(self) -> Optional[T]:
        raise StateBreak()

    def cmd_examine(self) -> Optional[T]:
        pass

    def cmd_equipment(self) -> Optional[T]:
        pass

    def cmd_inventory(self) -> Optional[T]:
        pass

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_pickup(self) -> Optional[T]:
        pass

    def cmd_quit(self) -> Optional[T]:
        raise SystemExit()

    def cmd_debug_1(self):
        pass

    def cmd_debug_2(self):
        pass

    def cmd_debug_3(self):
        pass

    def cmd_debug_4(self):
        pass