from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from ..manager import Manager
from .test_view import TestView

if TYPE_CHECKING:
    from tcod.console import Console
    from .view import View
    from ..game import Game


class InterfaceManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._ui_list = []
        self._current_view = None
        self._views: Dict[str, View] = {
            'TEST': TestView
            }
        self.transition('TEST')

    @property
    def current_view(self) -> View:
        return self._current_view

    def transition(self, view: str) -> None:
        self._current_view = self._views[view](self)

    def on_draw(self, console: Console) -> None:
        self._current_view.on_draw(console)
        for element in self._ui_list:
            element.on_draw(console)
