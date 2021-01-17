from __future__ import annotations
import time

from simulacra.ecs.ecs_manager import ECSManager as Engine

from .area_manager import AreaManager
from .camera_manager import CameraManager
from .console_manager import ConsoleManager
from .game_state_manager import GameStateManager
from .player_manager import PlayerManager
from .world_manager import WorldManager

from .rendering import RenderManager
from .input import CommandManager, InputController
from .interface import InterfaceManager


class Game:

    def __init__(self) -> None:
        self.engine = Engine(self)               # Working: 2021-01-16

        self.renderer = RenderManager(self)      # TODO
        self.state = GameStateManager(self)      # Working: 2021-01-17
        self.world = WorldManager(self)          # TODO
        self.area = AreaManager(self)            # TODO
        self.camera = CameraManager(self)        # TODO
        self.player = PlayerManager(self)        # TODO
        self.commands = CommandManager(self)     # Working: 2021-01-17
        self.interface = InterfaceManager(self)  # TODO
        self.input = InputController(self)       # Working: 2021-01-17
        self.console = ConsoleManager(self)      # Working: 2021-01-17

        self.action_system = None
        self.status_system = None
        self.render_system = None
        self.interface_system = None
        self.particle_system = None
        self.destroy_system = None
        self.ability_system = None

    def start(self) -> None:
        self.last_update = time.time()

    def update_engine_systems(dt):
        pass

    def update_player_systems(dt):
        pass

    def loop(self) -> None:
        while True:
            self.console.context.present(self.console.root_console)
            self.renderer.render()
            self.input.handle_input()
