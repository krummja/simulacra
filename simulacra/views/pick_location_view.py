from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from config import *
from view import View
from views.stage_view import StageView
from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from tcod.console import Console
    from entity import Entity
    from state import State


class PickLocationView(StageView):
    
    def __init__(self, state: State) -> None:
        super().__init__(state, state.model)
        
    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        cam_x, cam_y = self.state.model.area.camera.get_camera_pos()
        x = self.state.cursor_xy[0] - cam_x
        y = self.state.cursor_xy[1] - cam_y
        style = {"fg": (255, 255, 255), "bg": (0, 0, 0)}
        consoles['ROOT'].print(x+1, y, string=chr(9665), fg=(255, 150, 150))
        consoles['ROOT'].print_box(x+2, y, 12, 1, string=self.state.info.upper(), fg=(0, 0, 0), bg=(255, 150, 150))
        if 0 <= x < STAGE_PANEL_WIDTH and 0 <= y < STAGE_PANEL_HEIGHT:
            consoles['ROOT'].tiles_rgb.T[["fg", "bg"]][x, y] = (255, 0, 0), (0, 0, 0)
   