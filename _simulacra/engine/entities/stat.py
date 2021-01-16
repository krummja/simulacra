"""ENGINE.ENTITIES.Stat"""
from __future__ import annotations
from typing import Tuple

import math
from enum import Enum


class Stat:
    """Representation of a single stat, for use with a Stats component."""

    def __init__(self, stat: StatsEnum, current: float, maximum: float) -> None:
        if stat in StatsEnum:
            self.stat = stat
        else:
            raise AttributeError(f"{stat} is not a valid stat!")
        self.current = current
        self.maximum = maximum

    def modify_current(self, value: float) -> None:
        """Adjust the current value of the attribute."""
        self.current += value

    def modify_max(self, value: float) -> None:
        """Adjust the maximum possible value of the attribute."""
        self.maximum += value

    @property
    def display(self) -> Tuple[float, float]:
        return self.current, self.maximum

    def __str__(self) -> str:
        return str(self.current)

    def __int__(self) -> int:
        return int(self.current)


class StatModifier:
    """Representation of a modifier for a base Stat type."""

    def __init__(self, value: int, level_progression: int = 0) -> None:
        self.value = value
        self.level_progression = level_progression

    def __int__(self):
        # TODO: Implementation
        return

    def get_leveled_value(self, level, initial_level) -> int:
        if self.level_progression > 0:
            multiplier = (level - initial_level) / self.level_progression
            return math.ceil(self.value * multiplier)
        else:
            return self.value


class StatsEnum(Enum):
    Health = 'health'
    Energy = 'energy'
    Might = 'might'
    Finesse = 'finesse'
    Intellect = 'intellect'
    Sharpness = 'sharpness'
    Hardness = 'hardness'
    Weight = 'weight'
    Size = 'size'
    Potency = 'potency'
    MaxDamage = 'max_damage'
    MinDamage = 'min_damage'
    ArmorClass = 'armor_class'


class Size:
    Fine = 0
    Diminutive = 1
    Tiny = 2
    Small = 3
    Medium = 4
    Large = 5
    Huge = 6
    Gargantuan = 7
    Colossal = 8
