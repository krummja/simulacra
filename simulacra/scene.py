from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from abc import abstractmethod, ABCMeta
from managers.console_manager import ConsoleManager
from managers.scene_manager import SceneManager
from managers.game_context import GameContext


class BaseScene(metaclass=ABCMeta):
    
    def __init__(
            self, 
            console_manager: ConsoleManager, 
            scene_manager: SceneManager, 
            game_context: GameContext
        ) -> None:
        self.console_manager = console_manager
        self.scene_manager = scene_manager
        self.game_context = game_context
        
    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def handle_input(self):
        pass
    
    def transition_to(self, scene_name: str):
        self.scene_manager.transition_to(scene_name)