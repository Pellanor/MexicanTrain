from src.Domino import Domino


class BotDomino(tuple):
    @property
    def domino_id(self):
        return self[1]

    @property
    def value(self):
        return self[2]

    __slots__ = ()
    # An immutable and unique marker, used to make sure different
    # tuple subclasses are not equal to each other.
    _MARKER = object()

    def __new__(cls, domino_id, domino: Domino):
        return tuple.__new__(cls, (cls._MARKER, domino_id, domino))

    def __init__(self, domino_id, domino: Domino):
        super().__init__()
