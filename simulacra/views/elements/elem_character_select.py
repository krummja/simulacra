from __future__ import annotations
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

import numpy as np

from config import *
from panel import Panel

if TYPE_CHECKING:
    from tcod.console import Console
    from model import Model
    from storage import Storage


class ElemCharacterSlot(Panel):

    _slot_data: Model

    def __init__(
            self,
            parent: ElemCharacterSelect,
            position: Tuple[str, str],
        ) -> None:
        super().__init__(**{
            'parent': parent,
            'position': position,
            'size': {'width': 20, 'height': 7},
            'style': {'framed': True}
            })

    @property
    def slot_data(self) -> Dict[str, Any]:
        if self._slot_data is not None:
            character_name = self._slot_data.player.noun_text
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

    def draw(self, consoles: Dict[str, Console]) -> None:
        self.on_draw(consoles)
        consoles['ROOT'].print(x=self.x + 2, y=self.y + 1,
                               string=self.slot_data['name'])
        consoles['ROOT'].print(x=self.x + self.size_width - 3, y=self.y + 3,
                               string=self.slot_data['level'])
        consoles['ROOT'].print(x=self.x + 2, y=self.y + 3,
                               string=self.slot_data['background'])
        consoles['ROOT'].print(x=self.x + 2, y=self.y + 5,
                               string=self.slot_data['location'])


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
            'offset': {'y': 14},
            'size': {'width': 64, 'height': 16},
            'style': {'fg': (255, 255, 255)}
            })

        self.slot_0 = ElemCharacterSlot(self, ('top', 'left'))
        self.slot_3 = ElemCharacterSlot(self, ('bottom', 'left'))

        self.slot_1 = ElemCharacterSlot(self, ('top', 'center'))
        self.slot_4 = ElemCharacterSlot(self, ('bottom', 'center'))

        self.slot_2 = ElemCharacterSlot(self, ('top', 'right'))
        self.slot_5 = ElemCharacterSlot(self, ('bottom', 'right'))

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

        self.slot_0.slot_data = self.data_source.data_hook(0)
        self.slot_1.slot_data = self.data_source.data_hook(1)
        self.slot_2.slot_data = self.data_source.data_hook(2)
        self.slot_3.slot_data = self.data_source.data_hook(3)
        self.slot_4.slot_data = self.data_source.data_hook(4)
        self.slot_5.slot_data = self.data_source.data_hook(5)

        self.slot_0.style_fg = self.focused if self.current_index == (0, 0) else self.unfocused
        self.slot_3.style_fg = self.focused if self.current_index == (0, 1) else self.unfocused

        self.slot_1.style_fg = self.focused if self.current_index == (1, 0) else self.unfocused
        self.slot_4.style_fg = self.focused if self.current_index == (1, 1) else self.unfocused

        self.slot_2.style_fg = self.focused if self.current_index == (2, 0) else self.unfocused
        self.slot_5.style_fg = self.focused if self.current_index == (2, 1) else self.unfocused

        self.slot_0.draw(consoles)
        self.slot_1.draw(consoles)
        self.slot_2.draw(consoles)
        self.slot_3.draw(consoles)
        self.slot_4.draw(consoles)
        self.slot_5.draw(consoles)

        # for i in range(0, 6):
        #     slot = getattr(self, f"slot_{i}")
        #     slot.slot_data = self.data_source.data_hook(i)
        #     slot.draw(consoles)
        #     slot.style_fg = self.focused if self.index_as_int == i else self.unfocused

        # TODO: Huh, this feels really sluggish for some reason...
        # TODO: That's not right. Gotta figure out why that is.
        # TODO: I bet it's the looping, actually!
