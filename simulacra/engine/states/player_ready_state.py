from __future__ import annotations
from typing import Generic, Tuple, TYPE_CHECKING

from config import *

from content.actions import common
from engine.events.result_manager import ResultManager
from engine.events.action import Action
from engine.events.result import Result
from interface.data_manager import DataManager
from engine.rendering.effects_manager import EffectsManager
from .state import SaveAndQuit, StateBreak, T
from .area_state import AreaState
from .pick_location_state import PickLocationState
from .inventory_menu_state import InventoryMenuState
from .equipment_menu_state import EquipmentMenuState
from .effects_state import EffectsState

if TYPE_CHECKING:
    from engine.model import Model


class PlayerReadyState(Generic[T], AreaState[T]):

    NAME = "Player Ready"

    def __init__(
            self,
            model: Model
        ) -> None:
        super().__init__(
            DataManager(model),
            ResultManager(model),
            EffectsManager(model),
            model,
            )

    def cmd_move(self, x: int, y: int) -> Action:
        action = common.MoveStart(self._model.player, (x, y))
        action.success = True
        result = action.make_result(action)
        self.result_manager.add_result(result)
        return action

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_quit(self) -> None:
        raise StateBreak("PlayerReadyState")

    def cmd_inventory(self):
        inventory_data = self.data_manager.query(
            entity="PLAYER",
            component="INVENTORY")
        state = InventoryMenuState(inventory_data)
        return state.loop()

    def cmd_examine(self):
        state = PickLocationState(self._model, "", self._model.player.location.xy)
        cursor_xy: Tuple[int, int] = state.loop()

    def cmd_equipment(self):
        equipment_data = self.data_manager.query(
                entity="PLAYER",
                component="EQUIPMENT")
        state = EquipmentMenuState(equipment_data)
        return state.loop()

    def cmd_pickup(self):
        return common.Pickup(self._model.player)

    def cmd_debug_1(self):
        print("F1")

    def cmd_debug_2(self):
        print(self._view.inventory_panel._data)

    def cmd_debug_3(self):
        print("F3")

    def cmd_debug_4(self):
        print("F4")
