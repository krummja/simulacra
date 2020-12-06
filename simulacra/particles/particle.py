from __future__ import annotations
from typing import Tuple, Callable, Optional
from collections import defaultdict

from math import pi, sin, cos, sqrt
from random import uniform, randint


class Particle:
    """A single particle in a Particle Effect."""
    
    def __init__(
            self,
            chars: str,
            x: int,
            y: int,
            dx: int,
            dy: int,
            colors: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
            lifetime: int,
            move,
            next_color=None,
            next_char=None,
            on_create=None,
            on_each=None,
            on_destroy=None,
        ) -> None:
        color_switch = next_color is not None
        char_switch = next_char is not None
        
        self.chars = chars
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.colors = colors
        self.time = 0
        self.lifetime = lifetime
        self._move = move
        self._next_color = (self._default_next_color, next_color)[color_switch]
        self._next_char = (self._default_next_char, next_char)[char_switch]
        self._last = None
        self._on_create = on_create
        self._on_each = on_each
        self._on_destroy = on_destroy
    
    @staticmethod
    def _default_next_color(particle: Particle):
        """Default next color
        Linear progression through each tuple.
        """
        return particle.colors[(
            len(particle.colors) - 1 * particle.time // particle.lifetime
        )]
    
    @staticmethod
    def _default_next_char(particle: Particle):
        """Default next character
        Linear progression through each character.
        """
        return particle.chars[(
            len(particle.chars) - 1 * particle.time // particle.lifetime
            )]
    
    def last(self):
        """The last attributes returned for this particle.
        Typically these are used for clearing out the particle on the 
        next frame.
        """
        return self._last
        
    def next(self):
        """The set of attributes for this particle for the next frame.
        Returns a tuple of (character, x, y, fg, attribute, bg)
        """
        x, y = self._move(self)
        color = self._next_color(self)
        char = self._next_char(self)
        self._last = char, x, y, (color[0], color[1], color[2])
        self.time += 1
        
        # Trigger any configured events.
        if self.time == 1 and self._on_create is not None:
            self._on_create(self)
        elif self.lifetime == self.time and self._on_destroy is not None:
            self._on_destroy(self)
        elif self._on_each is not None:
            self._on_each(self)
        return self._last
        