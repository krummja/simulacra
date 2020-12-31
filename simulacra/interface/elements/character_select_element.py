from __future__ import annotations
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

import numpy as np

from config import *
from interface.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.model import Model
    from engine.storage import Storage


class CharacterSlotElement(BaseElement):

    _slot_data: Model

    def __init__(
            self,
            config: ElementConfig,
        ) -> None:
        super().__init__(config)

    @property
    def slot_data(self) -> Dict[str, Any]:
        if self._slot_data is not None:
            character_name = self._slot_data.player.name
        else:
            character_name = "<empty>"

        return {
            'name': character_name,
            'level': '',
            'background': '',
            'location': ''
            }

    @slot_data.setter
    def slot_data(self, value: Model) -> None:
        self._slot_data = value

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].print(
            x=self.x + 2, y=self.y + 1,
            string=self.slot_data['name'],
            fg=(255, 255, 255)
            )

        consoles['ROOT'].print(
            x=self.x + self.width - 3, y=self.y + 3,
            string=self.slot_data['level'],
            fg=(255, 255, 255)
            )

        consoles['ROOT'].print(
            x=self.x + 2, y=self.y + 3,
            string=self.slot_data['background'],
            fg=(255, 255, 255)
            )

        consoles['ROOT'].print(
            x=self.x + 2, y=self.y + 5,
            string=self.slot_data['location'],
            fg=(255, 255, 255)
            )


class CharacterSelectElement(BaseElement):

    _data_source: Storage = None

    rows: int = 3
    cols: int = 2
    menu_cells = np.arange(rows * cols).reshape(cols, rows)

    y_index: int = 0
    x_index: int = 0

    focused = (255, 0, 255)
    unfocused = (255, 255, 255)

    def __init__(self) -> None:
        super().__init__(ElementConfig(
            position=('center', 'center'),
            offset_y=14,
            width=64, height=16,
            fg=(255, 255, 255)
            ))

        style = {
            'parent': self,
            'width': 20,
            'height': 7,
            'framed': True,
            'fg': (255, 255, 255)
            }
        self.slot_0 = CharacterSlotElement(
            ElementConfig(position=('top', 'left'), **style))
        self.slot_1 = CharacterSlotElement(
            ElementConfig(position=('top', 'center'), **style))
        self.slot_2 = CharacterSlotElement(
            ElementConfig(position=('top', 'right'), **style))
        self.slot_3 = CharacterSlotElement(
            ElementConfig(position=('bottom', 'left'), **style))
        self.slot_4 = CharacterSlotElement(
            ElementConfig(position=('bottom', 'center'), **style))
        self.slot_5 = CharacterSlotElement(
            ElementConfig(position=('bottom', 'right'), **style))

    @property
    def data_source(self) -> Storage:
        """Return reference to the Storage object"""
        return self._data_source

    @data_source.setter
    def data_source(self, value: Storage) -> None:
        """Assign reference to Storage object"""
        self._data_source = value

    @property
    def current_index(self) -> Tuple[int, int]:
        """Return (y, x) data slot index"""
        return self.y_index, self.x_index

    @current_index.setter
    def current_index(self, value: Tuple[int, int]) -> None:
        """Set data slot indices to provided value"""
        self.y_index += value[1]
        self.y_index = max(0, min(self.y_index, self.cols-1))
        self.x_index += value[0]
        self.x_index = max(0, min(self.x_index, self.rows-1))

    @property
    def index_as_int(self) -> int:
        """Return the integer index for the current data slot"""
        return self.menu_cells[self.current_index]

    @property
    def data_at_index(self) -> Optional[Model]:
        """Return reference to the data at the selected data slot"""
        if self.data_source:
            return self._data_source.data_hook(self.index_as_int)
        else:
            raise Exception("No data source assigned to this menu!")

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        self.slot_0.slot_data = self.data_source.data_hook(0)
        self.slot_1.slot_data = self.data_source.data_hook(1)
        self.slot_2.slot_data = self.data_source.data_hook(2)
        self.slot_3.slot_data = self.data_source.data_hook(3)
        self.slot_4.slot_data = self.data_source.data_hook(4)
        self.slot_5.slot_data = self.data_source.data_hook(5)

        self.slot_0.frame_fg = self.focused if self.index_as_int == 0 else self.unfocused
        self.slot_1.frame_fg = self.focused if self.index_as_int == 1 else self.unfocused
        self.slot_2.frame_fg = self.focused if self.index_as_int == 2 else self.unfocused
        self.slot_3.frame_fg = self.focused if self.index_as_int == 3 else self.unfocused
        self.slot_4.frame_fg = self.focused if self.index_as_int == 4 else self.unfocused
        self.slot_5.frame_fg = self.focused if self.index_as_int == 5 else self.unfocused

        self.slot_0.draw(consoles)
        self.slot_1.draw(consoles)
        self.slot_2.draw(consoles)
        self.slot_3.draw(consoles)
        self.slot_4.draw(consoles)
        self.slot_5.draw(consoles)
