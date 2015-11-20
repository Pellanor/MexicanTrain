from src import Player
from src.Train import Train


class BotPlayer(tuple):

    @property
    def player_id(self):
        return self[1]

    @property
    def tile_count(self):
        return self[2]

    @property
    def train(self):
        return self[3]

    __slots__ = ()
    # An immutable and unique marker, used to make sure different
    # tuple subclasses are not equal to each other.
    _MARKER = object()

    def __new__(cls, player: Player, train: Train):
        return tuple.__new__(cls, (cls._MARKER, player.identity.id, len(player.dominoes), train))

    def __init__(self, player, bot_train):
        super().__init__()
