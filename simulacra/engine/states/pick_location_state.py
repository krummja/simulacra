from __future__ import annotations
from typing import Dict, Optional, Tuple, TYPE_CHECKING

import tcod
import time

from .state import State, T, SaveAndQuit, GameOverQuit, StateBreak
from .area_state import AreaState
from interface.views.pick_location_view import PickLocationView

if TYPE_CHECKING:
    from engine.model import Model


class PickLocationState(AreaState[Tuple[int, int]]):

    def __init__(
            self,
            model: Model,
            desc: str,
            start_xy: Tuple[int, int]
        ) -> None:
        super().__init__(model)
        self._model = model
        self._view = PickLocationView(self)
        self.start_xy = start_xy
        self.cursor_xy = start_xy
        self.desc = str(self.cursor_xy)
        self.info = str(self.model.area.nearby_actor_entities(*start_xy))

    def cmd_move(self, x: int, y: int) -> None:
        x += self.cursor_xy[0]
        y += self.cursor_xy[1]
        x = min(max(0, x), self.model.area.width - 1)
        y = min(max(0, y), self.model.area.height - 1)
        if not self.model.area.area_model.visible[y, x]:
            self.cursor_xy = self.cursor_xy
        else:
            self.cursor_xy = x, y
            self.model.area.camera.camera_pos = self.cursor_xy
        self.desc = str(self.cursor_xy)

        try:
            self.info = str(self.model.area.nearby_actor_entities(*self.cursor_xy))
        except KeyError:
            self.info = "---"

    def cmd_confirm(self) -> Tuple[int, int]:
        return self.cursor_xy

    def cmd_quit(self) -> None:
        raise StateBreak()
