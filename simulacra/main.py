from __future__ import annotations

import tcod

from simulacra.core import Game


def main():
    game = Game()
    print(game.state.current_state.name)

if __name__ == '__main__':
    main()
