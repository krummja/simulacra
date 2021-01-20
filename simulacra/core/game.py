from __future__ import annotations

from simulacra.ecs.ecs_manager import ECSManager as ECS
from simulacra.ecs.systems.render_system import RenderSystem

from .area_manager import AreaManager
from .camera_manager import CameraManager
from .player_manager import PlayerManager
from .world_manager import WorldManager
from .input import InputController
from .views import ViewManager
from .rendering import RenderManager
from .states import GameStateManager


class Options:
    CONSOLE_WIDTH: int = 90
    CONSOLE_HEIGHT: int = 45
    STAGE_WIDTH: int = 256
    STAGE_HEIGHT: int = 256
    STAGE_PANEL_WIDTH: int = (CONSOLE_WIDTH // 3) * 2
    STAGE_PANEL_HEIGHT: int = (CONSOLE_HEIGHT // 4) * 3
    SIDE_PANEL_WIDTH: int = CONSOLE_WIDTH - STAGE_PANEL_WIDTH
    SIDE_PANEL_HEIGHT: int = CONSOLE_HEIGHT
    LOG_PANEL_HEIGHT: int = (CONSOLE_HEIGHT // 4)
    DEBUG: bool = False
    DEVELOP: bool = True
    VIEW_RADIUS: int = 10 if DEBUG is False else 30


class Game:

    def __init__(self) -> None:
        self.ecs = ECS(self)                     # Working: 2021-01-16

        # Change to a Renderer class
        self.renderer = RenderManager(self)      # Working: 2021-01-17
        self.state = GameStateManager(self)      # Working: 2021-01-17
        self.world = WorldManager(self)          # TODO
        self.area = AreaManager(self)            # TODO
        self.camera = CameraManager(self)        # Working: 2021-01-19
        self.player = PlayerManager(self)        # TODO
        self.interface = ViewManager(self)       # Working: 2021-01-17
        self.input = InputController(self)       # Working: 2021-01-17

        self.action_system = None
        self.status_system = None
        self.render_system = RenderSystem(self)
        self.interface_system = None
        self.particle_system = None
        self.destroy_system = None
        self.ability_system = None

    def update_engine_systems(self):
        self.render_system.update()

    def update_player_systems(self):
        pass

    def loop(self) -> None:
        while True:
            self.renderer.context.present(self.renderer.root_console)
            self.update_engine_systems()
            self.input.handle_input()
