import copy


class GameSystem:

    def __init__(self, game):
        self.__game = game

    def place_domino(self, train, domino, player):
        train.add_domino(domino, player)

    def get_playable_trains(self, player):
        playable_trains = []
        for train in self.__game.trains:
            if train.can_player_add(player):
                playable_trains.append(train)
        return playable_trains

    def get_all_trains(self):
        return self.__game.trains

