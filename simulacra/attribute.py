from __future__ import annotations

import math
from stats import StatsEnum


class Attribute:

    def __init__(self, stat: StatsEnum, current: int, maximum: int) -> None:
        if stat in StatsEnum:
            self.stat = stat
        else:
            raise AttributeError(f"{stat} is not a valid stat!")
        self.current = current
        self.maximum = maximum

    def __str__(self) -> str:
        return str(self.current)

    def __int__(self) -> int:
        return int(self.current)

    def modify_current(self, value: int) -> None:
        self.current += value

    def modify_max(self, value: int) -> None:
        self.maximum += value


class StatModifier:

    def __init__(self, value: int, level_progression: int = 0) -> None:
        self.value = value
        self.level_progression = level_progression

    def __int__(self):
        return

    def get_leveled_value(self, level, initial_level) -> int:
        if self.level_progression > 0:
            multiplier = (level - initial_level) / self.level_progression
            return math.ceil(self.value * multiplier)
        else:
            return self.value
