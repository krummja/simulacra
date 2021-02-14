
class Tile:
    """Nonce class for a tile that has not been replaced by a concrete entity."""

    UNFORMED = True
    PASSABLE = True

    @property
    def passable(self) -> bool:
        return self.PASSABLE

    @passable.setter
    def passable(self, value: bool) -> None:
        self.PASSABLE = value

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        self.UNFORMED = False
        self._entity = value
