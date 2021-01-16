from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Tuple

import content.actions.move
import content.actions.pickup
from engine.events.action import Action

from .area_state import AreaState
from .equipment_menu_state import EquipmentMenuState
from .inventory_menu_state import InventoryMenuState
from .pick_location_state import PickLocationState
from .state import SaveAndQuit, StateBreak, T
from engine.events.result_manager import ResultManager
from engine.rendering.effects_manager import EffectsManager
from interface.data_manager import DataManager

if TYPE_CHECKING:
    from engine.model import Model


class PlayerReadyState(Generic[T], AreaState[T]):

    def __init__(
            self,
            model: Model
        ) -> None:
        self.managers = {
            'data': DataManager(model),
            'effects': EffectsManager(model),
            'results': ResultManager(model)
            }
        super().__init__(model)

    def cmd_move(self, x: int, y: int) -> Action:
        action = content.actions.move.MoveStart(self._model.player, (x, y))
        action.success = True
        result = action.make_result(action)
        self.managers['results'].add_result(result)
        return action

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_quit(self) -> None:
        raise StateBreak("PlayerReadyState")

    def cmd_inventory(self):
        inventory_data = self.managers['data'].query(
            entity="PLAYER",
            component="INVENTORY")
        state = InventoryMenuState(inventory_data)
        return state.loop()

    def cmd_examine(self):
        state = PickLocationState(
            self._model,
            self.managers,
            "",
            self._model.player.location.xy
            )
        state.loop()

    def cmd_equipment(self):
        equipment_data = self.managers['data'].query(
                entity="PLAYER",
                component="EQUIPMENT")
        state = EquipmentMenuState(equipment_data)
        return state.loop()

    def cmd_pickup(self):
        return content.actions.pickup.Pickup(self._model.player)

    def cmd_debug_1(self):
        print("F1")

    def cmd_debug_2(self):
        print(self._view.inventory_panel._data)

    def cmd_debug_3(self):
        print("F3")

    def cmd_debug_4(self):
        print("F4")
