from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from interface.views.effects_view import EffectsView
from .state import EffectsBreak
from .area_state import AreaState

if TYPE_CHECKING:
    from engine.areas import Location
    from engine.model import Model
    from interface import View


class EffectsState(AreaState[None]):

    def __init__(
            self,
            model: Model,
            effect = None
        ) -> None:
        super().__init__(model)
        self.effect = effect
        self._view = EffectsView(self, model)
        self.model.effect_flag = True

    def cmd_quit(self):
        raise EffectsBreak()
