from __future__ import annotations  # type: ignore
from typing import Any, Optional, Tuple, TYPE_CHECKING

import numpy as np
from interface.panel import Panel


class GridMenu(Panel):

    _data_source: Dict[int, Optional[Any]] = None

    def __init__(
            self,
            position: Optional[Tuple[str, str]]=None,
            parent: Optional[Panel]=None,
            width: int=0,
            height: int=0,
            margin: int=0,
            vertical_offset: int=0,
            horizontal_offset: int=0,
            fg: Tuple[int, int, int]=(255, 255, 255),
            bg: Tuple[int, int, int]=(0, 0, 0),
            columns: int=0, 
            rows: int=0,
        ) -> None:
        """The entries in the grid menu are stored as an integer array, which
        allows for easy navigation by hooking into the movement system.
        """
        super().__init__(
            position=position,
            parent=parent,
            width=width,
            height=height,
            margin=margin,
            vertical_offset=vertical_offset,
            horizontal_offset=horizontal_offset,
            fg=fg,
            bg=bg,
        )
        self.columns = columns
        self.rows = rows
        self.x_index: int = 0
        self.y_index: int = 0
        self.grid_cells = np.arange(columns * rows).reshape(columns, rows) 

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, value):
        self._data_source = value

    @property
    def current_index(self) -> Tuple[int, int]:
        return self.y_index, self.x_index

    @current_index.setter
    def current_index(self, offset: Tuple[int, int]) -> None:
        self.x_index += offset[0]
        self.y_index += offset[1]

        self.x_index = np.clip(self.x_index, 0, self.columns)
        self.y_index = np.clip(self.y_index, 0, self.rows)

    @property
    def data_at_index(self) -> int:
        if self.data_source:
            return self.data_source.data_hook(self.grid_cells[self.current_index])
        else:
            raise Exception("No data source assigned to this menu!")

    def on_draw(self) -> None:
        pass
        