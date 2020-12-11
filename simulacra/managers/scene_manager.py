from __future__ import annotations  # type: ignore
from typing import Dict, TYPE_CHECKING

import manager

if TYPE_CHECKING:
    from scene import BaseScene
    from managers.console_manager import ConsoleManager
    from managers.game_context import GameContext


class SceneManager(manager.BaseManager):
    
    def __init__(
            self,
            console_manager: ConsoleManager,
            game_context: GameContext
        ) -> None:
        super().__init__()
        self.console_manager = console_manager
        self.game_context = game_context
        self.current_scene: BaseScene = None
        self.scenes: Dict[str, BaseScene] = {}
        
    def transition_to(self, scene_name: str) -> None:
        self.current_scene = self.scenes[scene_name](self.console_manager,
                                                     self,
                                                     self.game_context)
        
    def render_current_scene(self, **kwargs):
        self.current_scene.render(**kwargs)
    
    def handle_input(self, **kwargs):
        self.current_scene.handle_input(**kwargs)