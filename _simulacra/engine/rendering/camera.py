"""ENGINE.RENDERING.Camera"""
from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import numpy as np

from config import STAGE_PANEL_WIDTH, STAGE_PANEL_HEIGHT

if TYPE_CHECKING:
    from engine.areas import Area


class Camera:
    """Utility class that provides views of the space around the player or
    active control (when not the player).
    """

    def __init__(self, area: Area) -> None:
        self.area = area
        self.camera_pos: Tuple[int, int] = (0, 0)

    def get_camera_pos(self) -> Tuple[int, int]:
        cam_x = self.camera_pos[0] - STAGE_PANEL_WIDTH // 2
        cam_y = self.camera_pos[1] - STAGE_PANEL_HEIGHT // 2
        return cam_x, cam_y

    def get_camera_view(self) -> Tuple[Tuple[slice, slice], Tuple[slice, slice]]:
        cam_x, cam_y = self.get_camera_pos()
        screen_left = max(0, -cam_x)
        screen_top = max(0, -cam_y)
        world_left = max(0, cam_x)
        world_top = max(0, cam_y)

        screen_width = min(STAGE_PANEL_WIDTH - screen_left,
                           self.area.width - world_left)
        screen_height = min(STAGE_PANEL_HEIGHT - screen_top,
                            self.area.height - world_top)

        screen_view = np.s_[screen_top:screen_top + screen_height,
                            screen_left:screen_left + screen_width]
        world_view = np.s_[world_top:world_top+screen_height,
                           world_left:world_left + screen_width]

        return screen_view, world_view
