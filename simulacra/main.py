from __future__ import annotations

import tcod.context

import config
from states.test_state import TestState


def main() -> None:
    with tcod.context.new_terminal(
            columns=config.CONSOLE_WIDTH,
            rows=config.CONSOLE_HEIGHT,
            tileset=config.TILESET,
            title="Simulacra",
            vsync=True
        ) as config.CONTEXT:

        while True:
            TestState().loop()


if __name__ == '__main__':
    main()
