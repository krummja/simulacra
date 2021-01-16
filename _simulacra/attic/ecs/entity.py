from __future__ import annotations
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ecs.engine import Engine
    from ecs.component import Component


class Entity:

    def __init__(self, uid: str, ecs: Engine) -> None:
        self.uid = uid
        self.ecs = ecs
        self.components: Dict[str, Component] = {}

    def destroy(self) -> None:
        pass

    def add(self, component: Component) -> None:
        pass

    def attach(self, component: Component) -> None:
        pass

    def remove(self, component: Component) -> None:
        pass
