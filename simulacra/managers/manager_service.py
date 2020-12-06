from __future__ import annotations
from typing import TYPE_CHECKING

from managers.animation_manager import AnimationManager
from managers.interface_manager import InterfaceManager
from managers.data_manager import DataManager
from managers.result_manager import ResultManager
from managers.effects_manager import EffectsManager

from util import Singleton

if TYPE_CHECKING:
    from model import Model


class ManagerService(metaclass=Singleton):

    def __init__(self) -> None:
        self.animation_manager = AnimationManager()
        self.interface_manager = InterfaceManager()
        self.result_manager = ResultManager()
        self.data_manager = None
    
    def initialize_managers(self, model: Model) -> None:
        self.data_manager = DataManager(model)
        self.effects_manager = EffectsManager(model)