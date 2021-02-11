from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from simulacra.core.options import *

from ..input.input_controller import T
from .screen import Screen
from .interface.surface import Surface


if TYPE_CHECKING:
    from .screen_manager import ScreenManager
    from simulacra.core.game import Game


class StageScreen(Screen):
    name: str = "STAGE"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.game: Game = manager.game

    def on_enter(self) -> None:
        self.game.camera.update(100)
        self.game.fov_system.update_fov()
        self.game.render_system.update(100)
        self.draw_ui(100)

    def on_update(self, dt) -> None:
        self.handle_input()
        self.game.update_engine_systems(dt)
        self.draw_ui(dt)

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        self.game.player.move((x, y))

    def cmd_confirm(self) -> Optional[T]:
        print("Command CONFIRM")

    def cmd_escape(self) -> None:
        self.cmd_quit()

    def draw_ui(self, dt) -> None:
        self.game.renderer.root_console.layer(5)
        self.draw_stage_panel_frame(dt)
        self.draw_fps_counter(dt)

    def draw_stage_panel_frame(self, dt):
        x_offset = (CONSOLE_WIDTH - STAGE_PANEL_WIDTH) // 2
        y_offset = 1
        self.game.renderer.root_console.color(0xFFFFFFFF)
        self.game.renderer.root_console.layer(self.game.renderer.layers['INTERFACE'])
        self.game.renderer.root_console.put(   0 + x_offset,  0 + y_offset, 0xEF04 + (16*0) )
        self.game.renderer.root_console.put( 120 + x_offset,  0 + y_offset, 0xEF06 + (16*0) )
        self.game.renderer.root_console.put(   0 + x_offset, 40 + y_offset, 0xEF04 + (16*2) )
        self.game.renderer.root_console.put( 120 + x_offset, 40 + y_offset, 0xEF06 + (16*2) )
        for x in range(0+x_offset, 120+x_offset, 2):
            self.game.renderer.root_console.put( 2 + x,  0 + y_offset, 0xEF05 + (16*0) )
            self.game.renderer.root_console.put( 2 + x, 40 + y_offset, 0xEF05 + (16*2) )
        for y in range(0+y_offset, 40+y_offset, 2):
            self.game.renderer.root_console.put(   0 + x_offset, 2 + y, 0xEF04 + (16*1) )
            self.game.renderer.root_console.put( 120 + x_offset, 2 + y, 0xEF06 + (16*1) )

        # Draw the stage panel shadow
        self.game.renderer.root_console.put( 0 + x_offset, 0 + y_offset + 42, 0xEF04 + (16*3) )
        self.game.renderer.root_console.put( 0 + x_offset + 124, 0 + y_offset, 0xEF07 + (16*0) )
        for x in range(0+x_offset+4, 121+x_offset, 2):
            self.game.renderer.root_console.put( 0 + x, 42 + y_offset, 0xEF05 + (16*3) )
        for y in range(0+y_offset, 39+y_offset, 2):
            self.game.renderer.root_console.put( 124 + x_offset, 2 + y, 0xEF07 + (16*1) )
        self.game.renderer.root_console.put( 124 + x_offset, 42 + y_offset, 0xEF07 + (16*3) )

    def draw_log_panel(self, dt):
        self.game.renderer.root_console.put( 1,   44, 0xEF00 + (16*0) )
        self.game.renderer.root_console.put( 102, 44, 0xEF02 + (16*0) )
        self.game.renderer.root_console.put( 1,   54, 0xEF00 + (16*2) )
        self.game.renderer.root_console.put( 102, 54, 0xEF02 + (16*2) )
        for x in range(0, 100, 4):
            self.game.renderer.root_console.put( 3+x, 44, 0xEF01 + (16*0) )
            self.game.renderer.root_console.put( 3+x, 54, 0xEF01 + (16*2) )
            for y in range(0, 8, 2):
                self.game.renderer.root_console.put( 3+x, 46+y, 0xEF01 + (16*1) )
        for y in range(0, 8, 2):
            self.game.renderer.root_console.put( 1,   46+y, 0xEF00 + (16*1) )
            self.game.renderer.root_console.put( 102, 46+y, 0xEF02 + (16*1) )

    def draw_fps_counter(self, dt):
        fps = self.game.fps.fps
        self.game.renderer.root_console.color(0xFFFF0000)
        self.game.renderer.root_console.puts(CONSOLE_WIDTH - 10, 0, "FPS: " + str(fps))
