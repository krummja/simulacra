from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from state import State


class StateManager:

    def __init__(self, console_manager) -> None:
        self.console_manager = console_manager
        self.current_state = None
        self.states = {}
        self.views = {}

    def add_state(self, state) -> None:
        self.states[state.__name__] = state

    def remove_state(self, state_name) -> None:
        if self.states[state_name]:
            del self.states[state_name]
        raise KeyError(f"No such state {state_name}!")

    def render_current_state(self, **kwargs) -> None:
        self.current_state.render(**kwargs)
