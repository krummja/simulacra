from __future__ import annotations
import time

import ecstremity as ecs

from .area_manager import AreaManager
from .camera_manager import CameraManager
from .console_manager import ConsoleManager
from .game_state_manager import GameStateManager
from .player_manager import PlayerManager
from .world_manager import WorldManager

from .rendering import RenderManager
from .input import CommandManager

class Game:

    last_update: int

    def __init__(self) -> None:
        self.engine = ecs.Engine()
        # self.clock = None
        self.renderer = RenderManager(self)
        self.state = GameStateManager(self)
        self.world = WorldManager(self)
        self.area = AreaManager(self)
        self.camera = CameraManager(self)
        self.player = PlayerManager(self)
        self.commands = CommandManager(self)
        # self.screens = ScreenManager
        # self.input = InputController
        self.console = ConsoleManager(self)

        self.action_system = None
        self.death_system = None
        self.status_system = None
        self.fov_system = None
        self.render_system = None
        self.ui_system = None
        self.particle_system = None
        self.fps_system = None
        self.destroy_system = None
        self.liquid_system = None
        self.fire_system = None
        self.temperature_system = None
        self.ability_system = None

    def start(self) -> None:
        self.last_update = time.time()

    def update_engine(self, dt: float) -> None:
        pass

    def update_player(self, dt: float) -> None:
        pass

    def loop(self) -> None:
        now = time.time()
        dt = now - self.last_update
        self.last_update = now
