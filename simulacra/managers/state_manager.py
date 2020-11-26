from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from state import State


class StateManager:

    def __init__(self) -> None:
        self.current_state = None
        self.states = {
            "MainMenu": MainMenuState
        }
        self.views = {
            "MainMenu": MainMenuView
        }

    def handle_input(self):
        pass

    def render_current_state(self, **kwargs) -> None:
        self.current_state.render(**kwargs)

    def transition_to(self, state_name) -> None:
        self.current_state = self.states[state_name]()