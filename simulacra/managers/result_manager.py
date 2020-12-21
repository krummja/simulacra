from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import states

if TYPE_CHECKING:
    from states import player_ready_state
    from action import Result
    from model import Model


class ResultManager:
    
    def __init__(self, model: Model) -> None:
        self.model = model
        self.results = []
        self.failures = []
        self.last_uid = 0
        self._cache_size = 100
    
    def add_result(self, result: Result) -> None:
        result.uid = self.last_uid + 1
        self.last_uid += 1
        
        # Check for messages to throw to the log
        if result.message:
            self.model.report(result.message)
        
        # Sort results into Failure and Success
        if result.success == False:
            self.failures.append(result)
        else:
            self.results.append(result)

        # if result.effect:
        #     state = states.effects_state.EffectsState(self.model)
        #     state.loop()

        # Do a little housekeeping to make things tidy
        if len(self.results) > self._cache_size:
            del self.results[0]
        if len(self.failures) > self._cache_size:
            del self.failures[0]

    def get_result(self) -> Result:
        result = self.results.pop()
        return result
