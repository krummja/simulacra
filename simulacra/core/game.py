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
        self.engine = Engine(self)

        self.renderer = RenderManager(self)
        self.state = GameStateManager(self)
        self.world = WorldManager(self)
        self.area = AreaManager(self)
        self.camera = CameraManager(self)
        self.player = PlayerManager(self)
        self.commands = CommandManager(self)
        self.interface = InterfaceManager(self)
        self.input = InputController(self)
        self.console = ConsoleManager(self)

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
            pass
