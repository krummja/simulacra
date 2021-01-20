from __future__ import annotations
from typing import Dict, Type, TYPE_CHECKING

from ..manager import Manager
from .test_view import TestView

if TYPE_CHECKING:
    from tcod.console import Console
    from .view import View
    from ..game import Game


class ViewManager(Manager):

    def __init__(self, game: Game) -> None:
        self.game = game
        self._ui_list = []
        self._current_view = None
        self._views: Dict[str, Type[View]] = {
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
