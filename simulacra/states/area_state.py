from __future__ import annotations
from typing import Dict, Generic, TYPE_CHECKING

from state import State, T
from views.stage_view import StageView

if TYPE_CHECKING:
    from managers.game_context import GameContext
    from tcod.console import Console
    from model import Model


class AreaState(Generic[T], State[T]):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self._model = model
        self._view = StageView(self, self._model)

    def draw(self, consoles: Dict[str, Console]) -> None:
        self.on_draw(consoles)
