from __future__ import annotations
from typing import Any, Generic, Optional, List, TYPE_CHECKING
from collections import UserList

import tcod

from .state import State, StateBreak, T
from interface.views.base_menu_view import BaseMenuView

if TYPE_CHECKING:
    from engine.model import Model
    from interface import View


class ListData:

    def __init__(self, data: List[Any]) -> None:
        self._data = data
        self._selection = 0

    @property
    def data(self) -> List[Any]:
        return self._data

    def __getitem__(self, index: int) -> str:
        if not isinstance(index, int):
            raise KeyError("The ListData class only supports int indexing!")
        if index <= 0:
            index = 0
        if len(self._data) <= index:
            index = len(self._data)
        selection = self._data[index]
        return selection

    def __len__(self) -> int:
        return len(self._data)


class BaseMenuState(Generic[T], State[T]):
    """Menu state that displays an indexed list that can be selected from.

    Parameters:
        view    -   the desired view of the data
        data    -   a list of entities, usually from a DataManager query

    -----------------
    | *  item1      |       _data = [<item1>, <item2>, <item3>, <item4>]
    | /  item2      |       0 <= _selection < 4
    | u  item3    4 |
    | !  item4      |
    -----------------
    """

    def __init__(self, view: View, data: List[Any]) -> None:
        super().__init__()
        self._view = view(self)
        self._data = data
        self._selection = 0

    @property
    def data(self) -> ListData:
        """Getter for classes outside of `BaseMenuState`. Encapsulates the
        data and provides similar functionality as the `BaseMenuClass` itself,
        e.g. setting bounds on indexing."""
        return ListData(self._data)

    @property
    def selection(self) -> int:
        return self._selection

    @selection.setter
    def selection(self, value: int) -> None:
        """Allow the `selection` attribute to be set within the bounds set by
        the length of the data list.
        """
        lower_bound = 0
        upper_bound = len(self.data) - 1
        if value <= lower_bound:
            value = lower_bound
        if upper_bound <= value:
            value = upper_bound
        self._selection = value

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        if event.sym in self.MOVE_KEYS:
            self.selection += self.MOVE_KEYS[event.sym][1]
        return super().ev_keydown(event)

    def cmd_confirm(self):
        pass