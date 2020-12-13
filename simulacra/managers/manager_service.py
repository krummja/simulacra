from __future__ import annotations
from typing import TYPE_CHECKING

from .data_manager import DataManager
from .result_manager import ResultManager
from .effects_manager import EffectsManager

from util import Singleton

if TYPE_CHECKING:
    from model import Model


class ManagerService(metaclass=Singleton):

    def __init__(self) -> None:
        self.data_manager = None
        self.effects_manager = None
        self.result_manager = None
    
    def initialize_managers(self, model: Model) -> None:
        self.data_manager = DataManager(model)
        self.effects_manager = EffectsManager(model)
        self.result_manager = ResultManager(model)