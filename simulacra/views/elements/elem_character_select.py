from __future__ import annotations
from typing import Dict, Optional, Tuple, TYPE_CHECKING

import numpy as np

from config import *
from panel import Panel

if TYPE_CHECKING:
    from tcod.console import Console
    from model import Model
    from storage import Storage


class ElemCharacterSelect(Panel):

    _data_source: Storage = None

    rows: int = 3
    cols: int = 2
    menu_cells = np.arange(rows * cols).reshape(rows, cols)

    x_index: int = 0
    y_index: int = 0

    focused = (255, 0, 255)
    unfocused = (255, 255, 255)

    def __init__(self) -> None:
        super().__init__(**{
            'position': ('center', 'center'),
            'offset': {'y': 16},
            'size': {'width': 64, 'height': 16},
            'style': {'fg': (255, 255, 255)}
            })

    @property
    def data_source(self) -> Storage:
        return self._data_source

    @data_source.setter
    def data_source(self, value: Storage) -> None:
        self._data_source = value

    @property
    def current_index(self) -> Tuple[int, int]:
        return self.y_index, self.x_index

    @current_index.setter
    def current_index(self, value: Tuple[int, int]) -> None:
        self.x_index += value[0]
        self.x_index = max(0, min(self.x_index, self.cols-1))
        self.y_index += value[1]
        self.y_index = max(0, min(self.y_index, self.rows-1))

    @property
    def index_as_int(self) -> int:
        return self.menu_cells[self.current_index]

    @property
    def data_at_index(self) -> Optional[Model]:
        if self.data_source:
            return self._data_source.data_hook(self.index_as_int)
        else:
            raise Exception("No data source assigned to this menu!")

    def draw(self, consoles: Dict[str, Console]) -> None:
        self.on_draw(consoles)
