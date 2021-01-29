from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

import math

from simulacra.utils.math_utils import mod
from simulacra.utils.geometry import Rect
from simulacra.utils.render_utils import *

from .manager import Manager
from simulacra.core.options import *

if TYPE_CHECKING:
    from .game import Game


class CameraManager(Manager):

    def __init__(self, game: Game) -> None:
        self._game = game
        self.width = 32
        self.height = 32
        self.padding = 0
        self.clamp_x = 32
        self.clamp_y = 20
        self._focus_x = 0
        self._focus_y = 0
        self.world_x = 0
        self.world_y = 0

    @property
    def rendered_tile_size(self):
        return SCALE * TILE_SIZE

    def compute_size(self):
        self.width = max(self.clamp_x,
                         math.floor(STAGE_PANEL_WIDTH / self.rendered_tile_size))
        self.height = max(self.clamp_y,
                          math.floor(STAGE_PANEL_HEIGHT / self.rendered_tile_size))
        self.world_x = math.floor(
            min(
                max(-self.padding, self._focus_x - self.width / 2),
                max((self.width - STAGE_WIDTH) / -2,
                    self.padding + STAGE_WIDTH - self.width)
                ))
        self.world_y = math.floor(
            min(
                max(-self.padding, self._focus_y - self.height / 2),
                max((self.height - STAGE_HEIGHT) / -2,
                    self.padding + STAGE_HEIGHT - self.height)
                ))

    def set_focus(self, x, y):
        self._focus_x = x
        self._focus_y = y
        self.compute_size()

    def set_padding(self, value):
        self.padding = value
        self.compute_size()

    def world_to_screen(self, x, y):
        return {
            'x': x - self.world_x,
            'y': y - self.world_y
            }

    def screen_to_world(self, x, y):
        return {
            'x': x + self.world_x,
            'y': y + self.world_y
            }

    @property
    def screen_rect(self):
        return {
            'x': self.world_x,
            'y': self.world_y,
            'width': self.width,
            'height': self.height
            }

    def is_in_view(self, world_x, world_y):
        screen = self.world_to_screen(world_x, world_y)
        return (
            screen['x'] < self.width and
            screen['y'] < self.height and
            screen['x'] >= 0 and
            screen['y'] >= 0
            )

    def update(self, dt):
        self.set_focus(*self._game.player.position)
