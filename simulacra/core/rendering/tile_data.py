from __future__ import annotations

import numpy as np


tile_graphic = np.dtype([
    ("ch", np.int),
    ("fg", "4B"),
    ("bg", "4B")
    ])


tile_dt = np.dtype([
    ("move_cost", np.uint8),
    ("transparent", np.bool),
    ("light", tile_graphic),
    ("dark", tile_graphic)
    ])
