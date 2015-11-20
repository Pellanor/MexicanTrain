from copy import copy

from src.Player import Player
from src.Train import Train


class BotTrain:

    def __init__(self, train: Train, player: Player):
        self.identity = train.identity
        self.am_owner = player == self.identity.owner
        self.can_add = train.can_player_add(player)
        self.cars = copy(train.cars)
        self.original_requires = self.requires = train.requires
        self.demands_satisfaction = train.demands_satisfaction

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.identity == other.identity

    def __hash__(self):
        return hash(self.identity)
