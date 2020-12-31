from __future__ import annotations
from typing import Generic, TYPE_CHECKING

from .state import State, T
from interface.views.stage_view import StageView

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.model import Model


class AreaState(Generic[T], State[T]):

    NAME = "Area"

    def __init__(
            self,
            data_manager,
            result_manager,
            effects_manager,
            model: Model
        ) -> None:
        super().__init__()
        self.data_manager = data_manager
        self.result_manager = result_manager
        self.effects_manager = effects_manager
        self._model = model
        self._view = StageView(self, self._model)
