from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class Attribute:

    def __init__(
            self,
            owner: Entity,
            name: str,
            base_value: int,
        ) -> None:
        self.owner = owner
        self._name = name
        self._base_value = base_value
        self._mod = 0
        self._current_value = None

    @property
    def name(self) -> str:
        """The name of the Attribute displayed in-game."""
        return self._name

    @property
    def base_value(self) -> int:
        """The starting value of the Attribute without a modifier."""
        return self._base_value

    @property
    def modifier(self) -> int:
        """An adjustment to the Attribute's base value."""
        return self._mod

    @modifier.setter
    def modifier(self, value: int) -> None:
        self._mod = value

    @property
    def mod_value(self) -> int:
        """The Attribute's starting value plus any applicable modifier
        value.
        """
        return self._base_value + self._mod

    @property
    def current_value(self) -> int:
        """The Attribute's current value."""
        if self._current_value is None:
            self._current_value = self.base_value + self.modifier
        if self._current_value > self._base_value:
            self._current_value = self._base_value + self.modifier
        return self._current_value

    @current_value.setter
    def current_value(self, value: int) -> None:
        self._current_value = value

    @property
    def current_over_base(self) -> float:
        return self._current_value / self.mod_value

    @property
    def percent_value(self) -> str:
        """The Attribute's current value represented as a percent."""
        dec = round(self._current_value / (self._base_value + self.modifier), 2)
        return f"{dec}"

    def __str__(self) -> str:
        return f"{self.current_value} / {self.mod_value}"

    def __repr__(self):
        return f"{self.current_value} / {self.mod_value}"
