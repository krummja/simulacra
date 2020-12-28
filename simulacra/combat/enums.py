"""Enums for Combat Engine"""

from enum import Enum


class TargetType(Enum):
    """Enumeration of different target shapes/behaviors."""
    Single = 0
    Cone = 1
    Radius = 2
    Beam = 3
    Missile = 4


class DamageType(Enum):
    """Enumeration of different damage types."""
    Blunt = 0
    Slash = 1
    Pierce = 2


class ThreatLevel(Enum):
    """Enumeration of how threatening an entity is."""
    Minor = 0
    Major = 1
    Critical = 2
    Fatal = 3
