from __future__ import annotations
from typing import TYPE_CHECKING

import math
from collections import deque
from functools import reduce

from simulacra.core.manager import Manager

if TYPE_CHECKING:
    from simulacra.core.game import Game


class FPSManager(Manager):

    frame_count = 60

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.fps = 0
        self.frames = deque([])
        for _ in range(self.frame_count):
            self.frames.append(0)

    def update(self, dt) -> None:
        self.frames.append(1000 / dt)
        self.frames.popleft()
        frame_sum = reduce((lambda s, v: s + v), self.frames)
        fps = math.trunc((frame_sum / self.frame_count) / 1000)
        self.fps = fps

        # 1612032459|444         JS
        # 1612032480|.1643255    PY
