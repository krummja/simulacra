from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class CameraManager(Manager):

    def __init__(self, game: Game) -> None:
        self.game = game
        self._area = self.game.area.current_area
        self._position: Tuple[int, int] = (0, 0)

    @property
    def position(self) -> Tuple[int, int]:
        cam_x = self._position[0]
        cam_y = self._position[1]
        return cam_x, cam_y

    @property
    def viewport(self) -> Tuple[Tuple[slice, slice], Tuple[slice, slice]]:
        cam_x, cam_y = self.position
