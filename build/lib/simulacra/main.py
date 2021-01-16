from __future__ import annotations
from ECStremity import Component, Engine


class Renderable(Component):

    name = "RENDERABLE"
    _render_order: int = 0

    def __init__(self, *, char: str, fg: str, bg: str) -> None:
        self.char = char
        self.fg = fg
        self.bg = bg

    def __lt__(self, other: Renderable) -> bool:
        return self._render_order < other._render_order


def main():
    engine = Engine()
    engine.register_component(Renderable)
    # engine.register_component(Position)

    renderable = engine.create_component(
        "RENDERABLE", {'char': '@', 'fg': '#fff', 'bg': '#000'}
        )
    print(renderable)

if __name__ == '__main__':
    main()
