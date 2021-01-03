from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from content.architect.decorator import Decorator
    from content.architect.architect import Architect
    from content.architect.architecture import Architecture
    from engine.geometry.rect import Rect


class Painter:
    """The procedural interface exposed by `Decorator` to let a `PaintStyle`
    modify the area."""

    def __init__(
            self,
            decorator: Decorator,
            architect: Architect,
            architecture: Architecture
        ) -> None:
        self._decorator = decorator
        self._architect = architect
        self._architecture = architecture
        self._painted: int = 0

    @property
    def bounds(self) -> Rect:
        return self._architect.area.shape
