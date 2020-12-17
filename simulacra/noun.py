from __future__ import annotations


class Noun:
    """The `Noun` class is a mixin for `Entity` objects.
    
    The goal of this class is to provide a consistent foundation for in-game
    reference to entities like Characters and Items.
    """
    
    def __init__(self) -> None:
        self._noun_text: str = "<unset>"

    def __str__(self) -> str:
        return self._noun_text