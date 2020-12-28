from __future__ import annotations


class Production:
    
    def __init__(self, left, right) -> None:
        """Represents a production consisting of a left and right side.
        
        Args:
            left (): graph object on the left side of the rule.
            right (): graph object on the right side of the rule.
        """
        self._left = left
        self._right = right
        
    def __str__(self):
        return str(self._left) + ' ==> ' + str(self.right) + '\n'
    
    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value
