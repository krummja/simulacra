from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.character import Character


class Attribute:

    def __init__(
            self, 
            owner: Character, 
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


# test_attribute = Attribute(None, "Test", 100)
# test_attribute.modifier = 10
# test_attribute.current_value -= 10

# print(f"Name:           {test_attribute.name}")
# print("---------------------------------")
# print(f"Base Value:     {test_attribute.base_value}")
# print(f"Modifier:       {test_attribute.modifier}")
# print(f"Mod Value:      {test_attribute.mod_value}")
# print(f"Current Value:  {test_attribute.current_value}")
# print(f"Percent Value:  {test_attribute.percent_value}")
# print(f"Raw Print:      {test_attribute}")