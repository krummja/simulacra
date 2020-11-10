from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from tcod import Console

from rendering import *
from view import View

if TYPE_CHECKING:
    from state import State
    from model import Model


class StageView(View):

    def __init__(self, state: State, model: Model) -> None:
        super().__init__(state)
        self.model = model

    def draw(self, consoles: Dict[str, Console]) -> None:
        area = self.model.area_data.current_area
        player = self.model.player
        if player.location:
            area.camera.camera_pos = player.location.xy

        update_fov(area)
        render_area_tiles(area, consoles)
        render_visible_entities(area, consoles)
