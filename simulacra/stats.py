from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum

import math


class Stat:

    def __init__(self, stat: StatsEnum, current: int, maximum: int) -> None:
        if stat in StatsEnum:
            self.stat = stat
        else:
            raise AttributeError(f"{stat} is not a valid stat!")
        self.current = current
        self.maximum = maximum

    def modify_current(self, value: int) -> None:
        """Adjust the current value of the attribute."""
        self.current += value

    def modify_max(self, value: int) -> None:
        """Adjust the maximum possible value of the attribute."""
        self.maximum += value
        
    def __str__(self) -> str:
        return str(self.current)

    def __int__(self) -> int:
        return int(self.current)
    
    # TODO: Implement other operators


class StatModifier:

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
