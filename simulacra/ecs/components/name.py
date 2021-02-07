from __future__ import annotations

from ecstremity import Component


class Name(Component):

    NAME_SET: bool = False
    ALLOW_CHANGE: bool = False

    def __init__(self) -> None:
        self._noun_text = ""

    @property
    def noun_text(self) -> str:
        return self._noun_text

    @noun_text.setter
    def noun_text(self, value: str) -> None:
        if not self.NAME_SET or self.ALLOW_CHANGE:
            self._noun_text = value
            self.NAME_SET = True
        else:
            pass
