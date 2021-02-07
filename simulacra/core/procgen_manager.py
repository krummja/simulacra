from __future__ import annotations
from typing import TYPE_CHECKING

import json

from apparata.parser import Generator

from simulacra.core.manager import Manager
from simulacra.core.options import *

if TYPE_CHECKING:
    from simulacra.core.game import Game


class ProcGenManager(Manager):

    def __init__(self, game: Game, report: bool = False) -> None:
        super().__init__(game)
        self.generator = Generator()

        self.current_area_data = self.game.world.current_area_data
        nodes, edges = self.generate_from_grammar('test.txt')
        self.current_area_data["nodes"] = nodes
        self.current_area_data["edges"] = edges

        if report:
            print(json.dumps(self.current_area_data, sort_keys=True, indent=2))

    def generate_from_grammar(self, grammar):
        parser = self.generator.generate_from_file(GRAMMAR_PATH + grammar)

        nodes = {}
        edges = {}

        for node, prop_dict in parser.nodes.items():
            node_data = f"{node}".split(", ")
            identifier = node_data[0]
            node_type = node_data[1]
            nodes[identifier] = {}

            for prop_key, prop_value in prop_dict.items():
                prop_key = f"{prop_key}".split(", ")
                key = prop_key[0]

                prop_value = f"{prop_value}".split(", ")
                if prop_value[1] == "NUMBER":
                    prop_value = int(prop_value[0])
                elif prop_value[1] == "ID":
                    prop_value = prop_value[0]
                nodes[identifier][key] = prop_value

        i = 0
        for (n, m), prop_dict in parser.edges.items():
            n_data = f"{n}".split(", ")
            m_data = f"{m}".split(", ")

            from_node = n_data[0]
            to_node = m_data[0]
            edges[i] = {"from": from_node, "to": to_node}

            for prop_key, prop_value in prop_dict.items():
                prop_key = f"{prop_key}".split(", ")
                key = prop_key[0]

                prop_value = f"{prop_value}".split(", ")
                if prop_value[1] == "NUMBER":
                    prop_value = int(prop_value[0])
                elif prop_value[1] == "ID":
                    prop_value = prop_value[0]
                edges[i][key] = prop_value
            i += 1

        return nodes, edges
