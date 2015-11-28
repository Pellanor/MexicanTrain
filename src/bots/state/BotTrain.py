from copy import copy

from src.Domino import Domino
from src.Player import Player
from src.Train import Train


class BotTrain:
    """
    The BotPlayer contains data accessible to bots on a given Player.
    The Bot cannot modify the Player by modifying the BotPlayer.
    """

    def __init__(self, train: Train, player: Player):
        self.identity = train.identity
        self.is_public = not train.private
        self.am_owner = player == self.identity.owner
        self.can_add = train.can_player_add(player)
        self.cars = copy(train.cars)
        self.requires = train.requires
        self.demands_satisfaction = train.demands_satisfaction
        if player is not None:
            self.owner_tile_count = len(player.dominoes)
        else:
            self.owner_tile_count = 0

    def play(self, domino: Domino) -> bool:
        """
        Add a domino to the current train, updating internal state as necessary.
        :param domino: the Domino to add
        :return: a boolean indicating if the domino was added successfully
        """
        if not domino.contains(self.requires):
            return False
        self.cars.append(domino)
        self.requires = domino.get_other_number(self.requires)
        self.demands_satisfaction = domino.is_double
        return True

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.identity == other.identity

    def __hash__(self):
        return hash(self.identity)

    def __str__(self):
        return "BotTrain {}\n Cars: {}".format(self.identity, self.cars)

    def __repr__(self):
        return "BotTrain {} -  Cars: {}".format(self.identity, self.cars)
