from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from action import Result


class ResultManager:
    
    def __init__(self) -> None:
        self.results = []
        self.last_uid = 0
    
    def add_result(self, result) -> None:
        result.uid = self.last_uid + 1
        self.results.append(result)
        self.last_uid += 1
        if len(self.results) > 100:
            self.results.pop()

    def get_result(self) -> Result:
        result = self.results.pop()
        return result