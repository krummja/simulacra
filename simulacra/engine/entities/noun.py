"""ENGINE.ENTITIES.Noun"""
from __future__ import annotations


class Noun:
    """The `Noun` class is a mixin for `Entity` objects.

    The goal of this class is to provide a consistent foundation for in-game
    reference to entities like Characters and Items.
    """

    def __init__(self) -> None:
        self._noun_text: str = "<unset>"

    @property
    def pronoun(self):
        return Pronoun.it


class Pronoun:
    """Representation of a pronoun."""

    nom: str
    obl: str
    gen: str

    def __init__(self, nom: str, obl: str, gen: str) -> None:
        self.nom = nom
        self.obl = obl
        self.gen = gen

    @classmethod
    def you(cls) -> Pronoun:
        return Pronoun('you', 'you', 'your')

    @classmethod
    def she(cls) -> Pronoun:
        return Pronoun('she', 'her', 'her')

    @classmethod
    def he(cls) -> Pronoun:
        return Pronoun('he', 'him', 'his')

    @classmethod
    def it(cls) -> Pronoun:
        return Pronoun('it', 'it', 'its')

    @classmethod
    def they(cls) -> Pronoun:
        return Pronoun('they', 'them', 'their')
