from __future__ import annotations
from typing import Any, List, Optional, TYPE_CHECKING

from content.actions import common
from interface.views.item_options_view import ItemOptionsView

from .base_menu_state import BaseMenuState
from interface.data_manager import DataManager

if TYPE_CHECKING:
    from engine.entities import Item
    from engine.entities.entity import Entity
    from engine.model import Model
    from interface import View


class ItemOptionsState(BaseMenuState["Action"]):

    def __init__(self, item: Item) -> None:
        self.data_manager = DataManager(self.model)
        self._item = item
        self._player = self.data_manager.query(entity="PLAYER")
        self._options = self._make_options()
        super().__init__(ItemOptionsView, self._options)

    def _make_options(self) -> List[Any]:
        _options = []
        if not self._item.is_equipped and self._item.owner is not None:
            _options.append('DROP')
        if self._item.is_equippable:
            _options.append('EQUIP')
        if self._item.is_equipped:
            _options.append('REMOVE')
        if len(_options) > 0:
            return _options
        else:
            pass

    def _opt_drop(self):
        return common.Drop(self._player, self._item)

    def _opt_equip(self):
        return common.Equip(self._player, self._item)

    def _opt_dequip(self):
        return common.Dequip(self._player, self._item)

    def cmd_confirm(self):
        if self._options[self._selection] == 'DROP':
            return self._opt_drop()
        if self._options[self._selection] == 'EQUIP':
            return self._opt_equip()
        if self._options[self._selection] == 'REMOVE':
            return self._opt_dequip()
