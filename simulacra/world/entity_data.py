from __future__ import annotations

import numpy as np
from simulacra.core.options import *


class EntityData:

    def __init__(self) -> None:
        self.shape = (STAGE_WIDTH, STAGE_HEIGHT)
        self.types = np.zeros(self.shape, dtype=object, order="F")

    def make_spawner(self, entity_type: str):
        pass
