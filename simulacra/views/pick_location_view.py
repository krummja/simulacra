from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from config import *
from view import View
from views.stage_view import StageView

if TYPE_CHECKING:
    from tcod.console import Console
    from entity import Entity
    from state import State


class PickLocationView(StageView):
    
    def __init__(self, state: State) -> None:
        super().__init__(state, state.model)
        
    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        
        style = {"fg": (255, 255, 255), "bg": (0, 0, 0)}
        consoles['ROOT'].print(0, 0, self.state.desc, **style)
        consoles['ROOT'].print(0, 2, self.state.info, **style)
        cam_x, cam_y = self.state.model.area.camera.get_camera_pos()
        x = self.state.cursor_xy[0] - cam_x
        y = self.state.cursor_xy[1] - cam_y
        if 0 <= x < STAGE_PANEL_WIDTH and 0 <= y < STAGE_PANEL_HEIGHT:
            consoles['ROOT'].tiles_rgb.T[["fg", "bg"]][x, y] = (255, 0, 0), (0, 0, 0)
   