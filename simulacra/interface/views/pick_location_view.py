from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import tcod

from config import *
from interface.elements.base_element import BaseElement, ElementConfig
from .view import View
from .stage_view import StageView

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.entities.entity import Entity
    from engine.states.state import State


class PickLocationView(StageView):

    def __init__(self, state: State) -> None:
        super().__init__(state, state.model)

    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        cam_x, cam_y = self.state.model.area.camera.get_camera_pos()
        x1 = self.state.start_xy[0] - cam_x
        y1 = self.state.start_xy[1] - cam_y
        x2 = self.state.cursor_xy[0] - cam_x
        y2 = self.state.cursor_xy[1] - cam_y


        style = {"fg": (255, 255, 255), "bg": (0, 0, 0)}
        consoles['ROOT'].print(1, 1, string=self.state.desc, **style)
        # consoles['ROOT'].print(x+1, y, string=chr(9665), fg=(255, 150, 150))
        # consoles['ROOT'].print_box(x1+2, y1, 12, 1, string=self.state.desc.upper(), fg=(0, 0, 0), bg=(255, 150, 150))

        if 0 <= x2 < STAGE_PANEL_WIDTH and 0 <= y2 < STAGE_PANEL_HEIGHT:
            consoles['ROOT'].tiles_rgb.T[["fg", "bg"]][x2, y2] = (0, 0, 0), (255, 0, 0)
        if 0 <= x2 < STAGE_PANEL_WIDTH and 0 <= y2 < STAGE_PANEL_HEIGHT:
            consoles['ROOT'].tiles_rgb.T[["fg", "bg"]][tcod.line_where(x1, y1, x2, y2)] = (0, 0, 0), (255, 0, 0)
