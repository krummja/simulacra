from __future__ import annotations
from typing import (List,
                    NewType,
                    Tuple)


import numpy as np
import tcod


Color = NewType('Color', Tuple[int, int, int])


class Colormap:
    
    def __init__(self) -> None:
        self._palette: List[Color] = []
    
    @property
    def palette(self) -> List[Color]:
        return self._palette
    
    @property
    def palette_indices(self) -> List[int]:
        return [_ for _ in range(len(self._palette))]