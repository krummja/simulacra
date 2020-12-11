from __future__ import annotations
from typing import (Dict,
                    Callable,
                    Generic,
                    Optional,
                    Tuple,
                    TypeVar,
                    TYPE_CHECKING)
import tcod
import config
import time
import threading

from autologging import logged
from rendering import frame_count, elapsed_time

from util import log
from factories.factory_service import FactoryService
from managers.manager_service import ManagerService

if TYPE_CHECKING:
    from tcod.console import Console
    from model import Model
    from storage import Storage
    from view import View

T = TypeVar("T")

start_time = time.time()

class RepeatedTimer:
    
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()
        
    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    
    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
    
    def stop(self):
        self._timer.cancel()
        self.is_running = False    
        

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

    NAME = "<base state>"
    
    factory_service = FactoryService()
    manager_service = ManagerService()
    
    _COMMAND_KEYS: Dict[int, str] = {
        tcod.event.K_d: "drop",
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

    LIMIT_FPS = 30
    TIC_SEC = 10
    TIC_SIZE = 1. / TIC_SEC
    FRAME_LEN = 1. / LIMIT_FPS

    def __init__(self) -> None:
        super().__init__()
        self._model: Optional[Model] = None
        self._storage: Optional[Storage] = None
        self._view: Optional[View] = None
        self.suspend = False
        self.last_tic = time.time()
        self.tic = 0
        
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

    def thread_time(self):
        return time.thread_time()
        
    def loop(self) -> Optional[T]:
        while True:

            # if time.time() >= self.TIC_SEC + self.last_tic:
            #     self.tic += 1
            #     self.last_tic = time.time()
                
            # if time.time() >= self.FRAME_LEN + self.last_tic:

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
            result = self.cmd_move(*self.MOVE_KEYS[event.sym])
            return result
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
