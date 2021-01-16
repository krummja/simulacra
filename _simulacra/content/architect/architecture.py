from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from content.architect.architect import Architect


class Architecture:
    """Each architecture is a separate algorithm and some tuning prameters
    for it that generates part of the area."""

    def __init__(self) -> None:
        self._architect: Architect = None
        self._style: ArchitecturalStyle = None
        self._region = None


class ArchitecturalStyle:

    def __init__(self) -> None:
        self._styles = None  # should be a ResourceSet
