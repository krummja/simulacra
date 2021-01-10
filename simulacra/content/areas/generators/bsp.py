from __future__ import annotations
from typing import Generator, List, Optional

from enum import Enum
import random
import tcod
import numpy as np

from content.areas.generators.generators import Algorithm
from engine.geometry.rect import Rect


class BinarySpacePartition(Algorithm):

    def __init__(
            self, *,
            depth: int,
            min_width: int,
            min_height: int,
            max_horizontal_ratio: float,
            max_vertical_ratio: float
        ) -> None:
        super().__init__()
        self.depth = depth
        self.min_width = min_width
        self.min_height = min_height
        self.max_horizontal_ratio = max_horizontal_ratio
        self.max_vertical_ratio = max_vertical_ratio

        self.bsp_data = []
        self.working = np.zeros((256, 256), dtype=np.int)

    def execute(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
        ) -> np.ndarray:
        bsp = tcod.bsp.BSP(x=x, y=y, width=width, height=height)
        bsp.split_recursive(
            depth=self.depth,
            min_width=self.min_width,
            min_height=self.min_height,
            max_horizontal_ratio=self.max_horizontal_ratio,
            max_vertical_ratio=self.max_vertical_ratio
            )

        for partition in bsp.in_order():
            if partition.children:
                self.bsp_data.append(partition)
            else:
                rect = Rect.from_edges(
                    left=partition.x,
                    top=partition.y,
                    right=partition.x + partition.w,
                    bottom=partition.y + partition.h
                    )
                yield rect
