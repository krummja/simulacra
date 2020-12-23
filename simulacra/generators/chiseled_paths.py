# https://github.com/BorisTheBrave/chiseled-random-paths/blob/master/main.ts
from __future__ import annotations
from typing import List, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from area import Area


neighbors = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
    ]


def find_articulation_points(area: Area, width: int, height: int):
    low = np.zeros((width, height))
    num: int = 1
    dfs_num = np.zeros((width, height))
    is_articulation = np.zeros((width, height), dtype=np.bool)
    
    def cut_vertex(ux: int, uy: int):
        child_count = 0
        
    
    return is_articulation