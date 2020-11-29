from __future__ import annotations
from typing import Dict, Generic, TYPE_CHECKING

from state import State, T
from views.stage_view import StageView

from ui_primitives.element_base import ElementBase
from ui_primitives.module_base import ModuleBase, ModuleRenderable

if TYPE_CHECKING:
    from tcod.console import Console
    from model import Model


class AreaState(Generic[T], State[T]):

    NAME = "Area"

    def __init__(self, model: Model) -> None:
        super().__init__()
        self._model = model
        self._view = StageView(self, self._model)
        
        self.test_element = ElementBase(name="TEST ELEMENT")
        self.test_module = ModuleBase(name="TEST MODULE", element=self.test_element)
        self.test_renderable = ModuleRenderable(module=self.test_module)
        test_element = self.manager_service.interface_manager.register_element(self.test_element)
        
        self.model.player.components['PHYSICS'].attach(self.test_module)