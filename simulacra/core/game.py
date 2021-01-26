from __future__ import annotations

import tcod
import time

from simulacra.ecs.ecs_manager import ECSManager as ECS
from simulacra.ecs.systems.render_system import RenderSystem
from simulacra.ecs.systems.action_system import ActionSystem
from simulacra.ecs.systems.fov_system import FOVSystem

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

        self.ecs = ECS(self)                     # Working: 2021-01-16

        self.clock = ClockManager(self)          # Working: 2021-01-20
        self.renderer = RenderManager(self)      # Working: 2021-01-17
        self.world = WorldManager(self)          # TODO
        self.camera = CameraManager(self)        # Working: 2021-01-19
        self.area = AreaManager(self)            # Working: 2021-01-21
        self.player = PlayerManager(self)        # Working: 2021-01-19
        self.screens = ScreenManager(self)       # Working: 2021-01-20
        self.input = InputController(self)       # Working: 2021-01-17
        self.ui = UIManager(self)                # TODO
        self.log = LogManager(self)              # TODO

        self.action_system = ActionSystem(self)
        self.status_system = None
        # self.fov_system = FOVSystem(self)
        self.render_system = RenderSystem(self)
        self.interface_system = None
        self.particle_system = None
        self.destroy_system = None
        self.ability_system = None

    def start(self):
        self._last_update = time.time()
        self.loop()
        self.renderer.root_console.close()

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
        # self.fov_system.update(dt)
        self.camera.update(dt)
        self.render_system.update(dt)
        # TODO Particle Update
        # TODO Map Update
        # TODO Log Update

    def loop(self) -> None:
        while True:
            now = time.time()
            dt = now - self._last_update

            self.renderer.root_console.refresh()
            self.screens.update(dt)
            self.ui.update(dt)

            self._last_update = now
