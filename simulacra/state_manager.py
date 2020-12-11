from __future__ import annotations
from typing import TYPE_CHECKING

from util import Singleton

if TYPE_CHECKING:
    from state import State


class StateManager(metaclass=Singleton):
    
    def __init__(self, init_state=None):
        self.states = []
        self.model = None
        self.cached_state = None
        self.current_state = init_state()
        
    def push_state(self, state):
        self.states.append(state)
    
    def pop_state(self):
        self.current_state = self.states.pop()
    
    def change_state(self, state, *args):
        self.push_state(self.current_state)
        self.current_state = state(*args)
        
    def remove_state(self, state):
        self.states.remove(state)
    
    def run_state(self):
        try:
            self.current_state.loop()
        except TypeError:
            self.current_state().loop()
        else:
            self.current_state(self.model).loop()
    
    def pause_state(self, state=None):
        self.cached_state = self.current_state
        if state is not None:
            self.current_state = state
        
    def restore_state(self):
        self.current_state = self.cached_state
    

