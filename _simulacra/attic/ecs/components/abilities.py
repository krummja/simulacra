from __future__ import annotations

from ecs.engine import Component


class Abilities(Component):

    def __init__(self, *, known, state) -> None:
        self.known = known
        self.state = state
