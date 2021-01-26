from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

import math

from simulacra.utils.math_utils import mod
from simulacra.utils.geometry import Rect

from .manager import Manager
from simulacra.core.options import *

if TYPE_CHECKING:
    from .game import Game


class CameraManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self._position: Tuple[int, int] = (0, 0)

        self.x = 0
        self.y = 0
        self.width = STAGE_PANEL_WIDTH
        self.height = STAGE_PANEL_HEIGHT

        self._camera_bounds: Rect = None
        self._render_offset = (0, 0)

        self._bounds = Rect.from_edges(
            left=self.x,
            top=self.y,
            right=self.width,
            bottom=self.height
            )

    @property
    def camera_bounds(self):
        return self._camera_bounds

    @property
    def render_offset(self):
        return self._render_offset

    @property
    def bounds(self):
        return self._bounds

    def position_camera(self):
        range_width = max(0, STAGE_WIDTH - STAGE_PANEL_WIDTH)
        range_height = max(0, STAGE_HEIGHT - STAGE_PANEL_HEIGHT)

        camera_range = Rect.from_edges(
            left=0,
            top=0,
            right=range_width,
            bottom=range_height
            )

        player_x = self._game.player.position[0]
        player_y = self._game.player.position[1]

        # The camera is positioned at player coordinates, offset by half the width of the
        # total viewport in both dimensions.
        camera = (
            player_x - ((STAGE_PANEL_WIDTH - 4) // 2),
            player_y - ((STAGE_PANEL_HEIGHT - 4) // 2)
            )

        camera = camera_range.clamp(camera[0] * 2, camera[1] * 2)

        self._camera_bounds = Rect.from_edges(
            left=camera[0],
            top=camera[1],
            right=camera[0] + min(STAGE_PANEL_WIDTH, STAGE_WIDTH),
            bottom=camera[1] + min(STAGE_PANEL_HEIGHT, STAGE_HEIGHT)
            )

        self._render_offset = (
            mod(max(0, STAGE_PANEL_WIDTH - STAGE_WIDTH), 2),
            mod(max(0, STAGE_PANEL_HEIGHT - STAGE_HEIGHT), 2)
            )

    def update(self, dt):
        self.position_camera()
