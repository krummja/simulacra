from __future__ import annotations

from ecs.engine import Component


class Renderable(Component):
    properties = ['char', 'fg', 'bg']

    _render_order: int = 0

    def __lt__(self, other: Renderable) -> bool:
        return self._render_order < other._render_order
