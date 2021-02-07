from __future__ import annotations
from typing import TYPE_CHECKING

from apparata.parser import Generator

from simulacra.core.manager import Manager
from simulacra.core.options import *

if TYPE_CHECKING:
    from simulacra.core.game import Game


class ProcGenManager(Manager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.generator = Generator()
        self.generate('test.txt')

    def generate(self, grammar):
        parser = self.generator.generate_from_file(GRAMMAR_PATH + grammar)

        nodes = {}
        edges = {}

        for node, prop_dict in parser.nodes.items():
            node = f"{node}".split(", ")
            node = node[0]
            nodes[node] = {}
            for prop, value in prop_dict.items():
                prop = f"{prop}".split(", ")
                prop = prop[0]

                value = f"{value}".split(", ")
                value = int(value[0]) if value[1] == "NUMBER" else value[0]

                nodes[node][prop] = value
        print(nodes)
