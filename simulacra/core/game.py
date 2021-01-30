from __future__ import annotations

import tcod
import time

from simulacra.ecs.ecs_manager import ECSManager as ECS
from simulacra.ecs.systems.render_system import RenderSystem
from simulacra.ecs.systems.action_system import ActionSystem
from simulacra.ecs.systems.fov_system import FOVSystem

from .rendering.fps_manager import FPSManager
from .area_manager import AreaManager
from .camera_manager import CameraManager
from .player_manager import PlayerManager
from .world_manager import WorldManager
from .clock_manager import ClockManager
from .log_manager import LogManager
from .screens import ScreenManager
from .input import InputController
from .rendering import RenderManager
from .screens.interface.ui_manager import UIManager


class Game:

    _last_update: float

    def __init__(self) -> None:

        self.ecs = ECS(self)

        self.clock = ClockManager(self)
        self.renderer = RenderManager(self)
        self.world = WorldManager(self)          # TODO
        self.camera = CameraManager(self)
        self.area = AreaManager(self)
        self.player = PlayerManager(self)
        self.screens = ScreenManager(self)
        self.input = InputController(self)
        self.ui = UIManager(self)                # TODO
        self.log = LogManager(self)              # TODO
        self.fps = FPSManager(self)

        self.action_system = ActionSystem(self)
        self.status_system = None
        # TODO self.fov_system = FOVSystem(self)
        self.render_system = RenderSystem(self)
        self.interface_system = None
        self.particle_system = None
        self.destroy_system = None
        self.ability_system = None

    def start(self):
        self.renderer.setup()

        self._last_update = time.time()
        self.loop()

        self.renderer.teardown()

    def update_engine_systems(self, dt):
        for _ in range(20):
            self.clock.update(dt)

            player_turn = self.action_system.update(dt)
            if player_turn:
                self.update_player_systems(dt)

            # TODO Run through systems

            if player_turn:
                return

    def update_player_systems(self, dt):
        # TODO self.fov_system.update(dt)
        self.camera.update(dt)
        self.render_system.update(dt)
        # TODO Particle Update
        # TODO Map Update
        # TODO Log Update

    def loop(self) -> None:
        while True:
            now = time.time()
            dt = now - self._last_update

            self.screens.update(dt)
            self.ui.update(dt)
            self.fps.update(dt)
            self.renderer.root_console.refresh()

            self._last_update = now
