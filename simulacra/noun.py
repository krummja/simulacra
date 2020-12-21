from __future__ import annotations


class Noun:
    """The `Noun` class is a mixin for `Entity` objects.

    The goal of this class is to provide a consistent foundation for in-game
    reference to entities like Characters and Items.
    """

    def __init__(self) -> None:
        self._noun_text: str = "<unset>"

    # def __str__(self) -> str:
    #     return self._noun_text

    @property
    def pronoun(self):
        return Pronoun.it


class Pronoun:

    nom: str
    obl: str
    gen: str

    def __init__(self, nom: str, obl: str, gen: str) -> None:
        self.nom = nom
        self.obl = obl
        self.gen = gen

    @classmethod
    def you(self) -> Pronoun:
        return Pronoun('you', 'you', 'your')

    @classmethod
    def she(self) -> Pronoun:
        return Pronoun('she', 'her', 'her')

    @classmethod
    def he(self) -> Pronoun:
        return Pronoun('he', 'him', 'his')

    @classmethod
    def it(self) -> Pronoun:
        return Pronoun('it', 'it', 'its')

    @classmethod
    def they(self) -> Pronoun:
        return Pronoun('they', 'them', 'their')
