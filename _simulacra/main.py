#!/usr/bin/env python3
from __future__ import annotations

import sys
import warnings
import tcod

from config import (SCREEN_WIDTH, SCREEN_HEIGHT)

from graphics.tilemap import Tilemap


def main() -> None:
    
    tilemap = Tilemap()
    
    context = tcod.context.new_window(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        tileset=tilemap.tilesheet,
        title="Simulacra",
        renderer=tcod.RENDERER_SDL2,
        vsync=True
        )
    
    console = tcod.Console(*context.recommended_console_size())
    
    while True:
        console.clear()
        console.print(1, 1, "Hello, world!")
        context.present(console, keep_aspect=True, integer_scaling=True)

if __name__ == '__main__':
    main()