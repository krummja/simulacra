from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import tcod



class StateBreak:
    """Return"""


class TestState(tcod.event.EventDispatch):
    
    _KEYS = {
        tcod.event.K_RETURN: "fire",
        tcod.event.K_ESCAPE: "escape"
    }
    
    def __init__(self) -> None:
        self._model = None
        self._view = None
        
    def loop(self):
        while True:
            self.on_draw(config.CONSOLES)
            for input_event in tcod.event.get():
                try:
                    value = self.dispatch(input_event)
                except StateBreak:
                    return None
                if value is not None:
                    return value
            
    def on_draw(self, consoles):
        pass
    
    def ev_quit(self, event):
        return self.cmd_quit()
    
    def ev_keydown(self, event):
        func = None
        if event.sym in self._KEYS:
            func = getattr(self, f"cmd_{self._KEYS[event.sym]}")
            return func()
        return None

    def cmd_fire(self):
        print("Fire!")
    
    def cmd_quit(self):
        raise SystemExit()



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


if __name__ == "__main__":
    main()