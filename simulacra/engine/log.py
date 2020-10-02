from __future__ import annotations


class Noun:

    def __init__(self: Noun, noun_text: str) -> None:
        self.noun_text = noun_text


class Pronoun:

    def __init__(self: Pronoun, nom: str, obl: str, gen: str) -> None:
        self.nom = nom
        self.obl = obl
        self.gen = gen

    @classmethod
    def you(cls: Pronoun) -> Pronoun:
        return Pronoun('you', 'you', 'your')

    @classmethod
    def she(cls: Pronoun) -> Pronoun:
        return Pronoun('she', 'her', 'her')

    @classmethod
    def he(cls: Pronoun) -> Pronoun:
        return Pronoun('he', 'him', 'his')

    @classmethod
    def it(cls: Pronoun) -> Pronoun:
        return Pronoun('it', 'it', 'its')

    @classmethod
    def they(cls: Pronoun) -> Pronoun:
        return Pronoun('they', 'them', 'their')


# TODO: Implement Log class
class Log:
    pass


class Message:

    def __init__(self: Message, text: str) -> None:
        self.text = text
        self.count = 1

    def __str__(self: Message) -> str:
        if self.count > 1:
            return f"{self.text} (x{self.count})"
        return self.text
