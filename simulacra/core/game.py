from __future__ import annotations

import time

from simulacra.utils.debug import debug, debugmethods

from simulacra.ecs.ecs_manager import ECSManager as ECS
from simulacra.ecs.systems.render_system import RenderSystem
from simulacra.ecs.systems.action_system import ActionSystem

from .area_manager import AreaManager
from .camera_manager import CameraManager
from .player_manager import PlayerManager
from .world_manager import WorldManager
from .clock_manager import ClockManager
from .screens import ScreenManager
from .input import InputController
from .rendering import RenderManager


class Game:

    _last_update: float

    def __init__(self) -> None:

        self.ecs = ECS(self)                     # Working: 2021-01-16

        self.clock = ClockManager(self)          # Working: 2021-01-20
        self.renderer = RenderManager(self)      # Working: 2021-01-17
        self.world = WorldManager(self)          # TODO
        self.area = AreaManager(self)            # TODO
        self.camera = CameraManager(self)        # Working: 2021-01-19
        self.player = PlayerManager(self)        # Working: 2021-01-19
        self.screens = ScreenManager(self)       # Working: 2021-01-20
        self.input = InputController(self)       # Working: 2021-01-17

        self.action_system = ActionSystem(self)
        self.status_system = None
        self.render_system = RenderSystem(self)
        self.interface_system = None
        self.particle_system = None
        self.destroy_system = None
        self.ability_system = None

    def start(self):
        self._last_update = time.time()
        self.loop()

    def update_engine_systems(self, dt):
        for _ in range(20):
            self.clock.update(dt)

            player_turn = self.action_system.update(dt)
            if player_turn:
                self.update_player_systems(dt)

            #! Run through systems

            if player_turn:
                return

    def update_player_systems(self, dt):
        self.render_system.update(dt)

    def loop(self) -> None:
        while True:
            now = time.time()
            dt = now - self._last_update

            self.screens.update(dt)
                # ScreenManager.update(dt)
                #   -> Screen.on_update(dt)
                #       -> game.update_engine_systems(dt)
            self._last_update = now
            self.renderer.context.present(self.renderer.root_console)
