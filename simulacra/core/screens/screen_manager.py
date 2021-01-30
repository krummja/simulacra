from __future__ import annotations
from typing import List, Dict, Optional, TYPE_CHECKING

from simulacra.core.manager import Manager
from .stage_screen import StageScreen
from .main_menu_screen import MainMenuScreen

if TYPE_CHECKING:
    from tcod.console import Console
    from simulacra.core.game import Game
    from .screen import Screen


class ScreenManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._stack: List[Screen] = []
        self._screens: Dict[str, Screen] = {
            'MAIN MENU': MainMenuScreen(self),
            'STAGE': StageScreen(self),
        }
        self.set_screen('MAIN MENU')

    @property
    def current_screen(self) -> Screen:
        return self._stack[-1]

    def set_screen(self, screen: str) -> None:
        """Dump the current stack if there is one and push a new screen."""
        while len(self._stack) > 0:
            self.current_screen.on_leave()
            self._stack.pop()
        self._stack.append(self._screens[screen])
        self.current_screen.on_enter()

    def replace_screen(self, screen: str) -> None:
        """Equivalent to a pop_screen followed by a push_screen."""
        self.current_screen.on_leave()
        self._stack.pop()
        self._stack.push(self._screens[screen])
        self.current_screen.on_enter()

    def push_screen(self, screen: str) -> None:
        """Push a screen onto the top of the stack."""
        self.current_screen.on_leave()
        self._stack.append(self._screens[screen])
        self._game.input._current_screen = self.current_screen
        self.current_screen.on_enter()

    def pop_screen(self) -> Screen:
        """Remove the highest screen from the stack."""
        self.current_screen.on_leave()
        self._stack.pop()
        self.current_screen.on_enter()

    def update(self, dt) -> None:
        self.current_screen.on_update(dt)
