from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

import numpy as np

from .manager import Manager
from simulacra.core.options import Options

if TYPE_CHECKING:
    from .game import Game


class CameraManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._position: Tuple[int, int] = (0, 0)

    @property
    def position(self) -> Tuple[int, int]:
        cam_x = self._position[0] - Options.STAGE_PANEL_WIDTH // 2
        cam_y = self._position[1] - Options.STAGE_PANEL_HEIGHT // 2
        return cam_x, cam_y

    @position.setter
    def position(self, value: Tuple[int, int]) -> None:
        self._position = value

    @property
    def viewport(self) -> Tuple[Tuple[slice, slice], Tuple[slice, slice]]:
        cam_x, cam_y = self.position
        screen_left = max(0, -cam_x)
        screen_top = max(0, -cam_y)
        world_left = max(0, cam_x)
        world_top = max(0, cam_y)

        screen_width = min(
            Options.STAGE_PANEL_WIDTH - screen_left,
            self._game.area.current_area.width - world_left
            )

        screen_height = min(
            Options.STAGE_PANEL_HEIGHT - screen_top,
            self._game.area.current_area.height - world_top
            )

        screen_view = np.s_[
                      screen_top:screen_top + screen_height,
                      screen_left:screen_left + screen_width
                      ]

        world_view = np.s_[
                     world_top:world_top + screen_height,
                     world_left:world_left + screen_width
                     ]

        return screen_view, world_view
