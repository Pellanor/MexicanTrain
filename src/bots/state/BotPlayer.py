from src import Player
from src.Train import Train


class BotPlayer(tuple):
    """
    The BotPlayer contains data accessible to bots on a given Player.
    The Bot cannot modify the Player by modifying the BotPlayer.
    """

    @property
    def player_id(self):
        return self[1]

    @property
    def tile_count(self):
        return self[2]

    @property
    def train(self):
        return self[3]

    @property
    def is_me(self):
        return self[4]

    __slots__ = ()
    # An immutable and unique marker, used to make sure different
    # tuple subclasses are not equal to each other.
    _MARKER = object()

    def __new__(cls, player: Player, train: Train, is_me):
        return tuple.__new__(cls, (cls._MARKER, player.identity.id, len(player.dominoes), train, is_me))

    def __init__(self, player, bot_train, is_me):
        super().__init__()
